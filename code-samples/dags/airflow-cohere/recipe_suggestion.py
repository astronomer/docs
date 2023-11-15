from airflow.decorators import dag, task
from airflow.models.param import Param
from airflow.models.baseoperator import chain
from airflow.providers.cohere.hooks.cohere import CohereHook
from airflow.providers.cohere.operators.embedding import CohereEmbeddingOperator
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.decomposition import PCA
from adjustText import adjust_text
from pendulum import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


COHERE_CONN_ID = "cohere_default"
IMAGE_PATH = "include/recipe_plot.png"


@dag(
    start_date=datetime(2023, 11, 1),
    schedule=None,
    catchup=False,
    params={
        "countries": Param(
            ["Switzerland", "Norway", "New Zealand", "Cameroon", "Bhutan", "Chile"],
            type="array",
            title="Countries of recipe origin",
            description="Enter from which countries you would like to get recipes. List at least two countries.",
        ),
        "pantry_ingredients": Param(
            ["gruyere", "olives", "potatoes", "onions", "pineapple"],
            type="array",
            description="List the ingredients you have in your pantry, you'd like to use",
        ),
        "type": Param(
            "vegetarian",
            type="string",
            enum=["vegan", "vegetarian", "omnivore"],
            description="Select the type of recipe you'd like to get.",
        ),
        "max_tokens_recipe": Param(
            500,
            type="integer",
            description="Enter the max number of tokens the model should generate.",
        ),
        "randomness_of_recipe": Param(
            25,
            type="integer",
            description=(
                "Enter the desired randomness of the recipe on a scale"
                + "from 0 (no randomness) to 50 (full randomness). "
                + "This setting corresponds to 10x the temperature setting in the Cohere API."
            ),
        ),
    },
)
def recipe_suggestions():
    @task
    def get_countries_list(**context):
        "Pull the list of countries from the context."
        countries = context["params"]["countries"]
        return countries

    @task
    def get_ingredients_list(**context):
        "Pull the list of ingredients from the context."
        ingredients = context["params"]["pantry_ingredients"]
        return ingredients

    @task
    def get_a_recipe(
        cohere_conn_id: str, country: str, ingredients_list: list, **context
    ):
        "Get recipes from the Cohere API for your pantry ingredients for a given country."
        type = context["params"]["type"]
        max_tokens_answer = context["params"]["max_tokens_recipe"]
        randomness_of_answer = context["params"]["randomness_of_recipe"]
        co = CohereHook(conn_id=cohere_conn_id).get_conn

        response = co.generate(
            model="command",
            prompt=f"Please provide a delicious {type} recipe from {country} "
            + f"that uses as many of these ingredients: {', '.join(ingredients_list)} as possible, "
            + "if you can't find a recipe that uses all of them, suggest an additional desert."
            + "Bonus points if it's a traditional recipe from that country, "
            + "you can name the city or region it's from and you can provide "
            + "vegan alternatives for the ingredients." 
            + "Provide the full recipe with all steps and ingredients.",
            max_tokens=max_tokens_answer,
            temperature=randomness_of_answer / 10,
        )

        recipe = response.generations[0].text

        print(f"Your recipe from {country}")
        print(f"for the ingredients {', '.join(ingredients_list)} is:")
        print(recipe)

        with open(f"include/{country}_recipe.txt", 'w') as f:
            f.write(recipe)

        return recipe

    countries_list = get_countries_list()
    ingredients_list = get_ingredients_list()
    recipes_list = get_a_recipe.partial(
        cohere_conn_id=COHERE_CONN_ID, ingredients_list=ingredients_list
    ).expand(country=countries_list)

    get_embeddings = CohereEmbeddingOperator.partial(
        task_id="get_embeddings",
        conn_id=COHERE_CONN_ID,
    ).expand(input_text=recipes_list)

    @task
    def plot_embeddings(embeddings, text_labels, file_name="embeddings_plot.png"):
        "Plot the embeddings of the recipes."

        embeddings = [x[0] for x in embeddings]
        print(text_labels)

        pca = PCA(n_components=2)
        reduced_embeddings = pca.fit_transform(embeddings)

        plt.figure(figsize=(10, 8))
        df_embeddings = pd.DataFrame(reduced_embeddings, columns=["PC1", "PC2"])
        sns.scatterplot(
            df_embeddings, x="PC1", y="PC2", s=100, color="gold", edgecolor="black"
        )

        font_style = {"color": "black"}
        texts = []
        for i, label in enumerate(text_labels):
            texts.append(
                plt.text(
                    reduced_embeddings[i, 0],
                    reduced_embeddings[i, 1],
                    label,
                    fontdict=font_style,
                    fontsize=15,
                )
            )

        # prevent overlapping labels
        adjust_text(texts, arrowprops=dict(arrowstyle="->", color="red"))

        distances = euclidean_distances(reduced_embeddings)
        np.fill_diagonal(distances, np.inf)  # exclude cases where the distance is 0

        n = distances.shape[0]
        distances_list = [
            (distances[i, j], (i, j)) for i in range(n) for j in range(i + 1, n)
        ]

        distances_list.sort(reverse=True)

        legend_handles = []
        for dist, (i, j) in distances_list:
            (line,) = plt.plot(
                [reduced_embeddings[i, 0], reduced_embeddings[j, 0]],
                [reduced_embeddings[i, 1], reduced_embeddings[j, 1]],
                "gray",
                linestyle="--",
                alpha=0.3,
            )
            legend_handles.append(line)

        legend_labels = [
            f"{text_labels[i]} - {text_labels[j]}: {dist:.2f}"
            for dist, (i, j) in distances_list
        ]

        for i in range(len(reduced_embeddings)):
            for j in range(i + 1, len(reduced_embeddings)):
                plt.plot(
                    [reduced_embeddings[i, 0], reduced_embeddings[j, 0]],
                    [reduced_embeddings[i, 1], reduced_embeddings[j, 1]],
                    "gray",
                    linestyle="--",
                    alpha=0.5,
                )

        plt.legend(
            legend_handles,
            legend_labels,
            title="Distances",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
        )

        plt.tight_layout()
        plt.title(
            "2D Visualization of recipe similarities", fontsize=16, fontweight="bold"
        )
        plt.xlabel("PCA Component 1", fontdict=font_style)
        plt.ylabel("PCA Component 2", fontdict=font_style)

        plt.savefig(file_name, bbox_inches="tight")
        plt.close()

    chain(
        get_embeddings,
        plot_embeddings(
            get_embeddings.output,
            text_labels=countries_list,
            file_name=IMAGE_PATH,
        ),
    )


recipe_suggestions()
