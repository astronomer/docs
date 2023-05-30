---
sidebar_label: Custom cell configuration reference
title: Custom cell configuration reference
id: custom-cell-reference
description: Learn how to configure a custom cell type as JSON.
---

This page contains reference information about all available JSON configurations for the custom operator cell type in the Astro Cloud IDE.  You enter this JSON when you create a new custom operator cell type in the Astro Cloud IDE. See [Create custom operator cells](cloud-ide/use-airflow-operators.md#create-custom-operator-cells) for setup steps.

## Display JSON reference

The following table is a reference for all possible key-value pairs in the `display` section of the JSON request.


| Name          | Type   | Description                                       |
| ------------- | ------ | ------------------------------------------------- |
| `label`       | String | The label to show in the **Add Cell** menu.       |
| `description` | String | The description to show in the **Add Cell** menu. |


## Behavior JSON reference

The following table is a reference for all possible key-value pairs in the `behavior` section of the JSON request.

| Name               | Type                                 | Description                                                                                                                                                                        |
| ------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `runnable`         | Boolean                              | Determines whether the cell type is runnable.                                                                                                                                      |
| `generatesData`    | Boolean                              | Determines whether the cell type generates data for XComs.                                                                                                                         |
| `namingStrategy`   | String, either `increment` or `uuid` | Determines how the default names are generated for new cells.                                                                                                                      |
| `excludeFromGraph` | Boolean                              | Determines whether to hide instances of the cell from the graph view of your pipeline editor.                                                                                      |
| `returnsRawValue`  | Boolean                              | Indicates whether the custom operator returns a raw value. Set to `true` if the operator uses TaskFlow. If set to false, `.output` is appended to the name of the operator output. |


## Generation JSON reference

The following table is a reference for all possible key-value pairs in the `generation` section of the JSON request.

| Name               | Type                                 | Description                                                                                                                                                                        |
| ------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`         | String, only option is `invoke`.                              | Determines how the operator is called.                                                                                                                                      |
| `invoke`    | Key-value pairs                              | The configuration for how the operator is invoked. Set `functionName` (String), `imports` (List of Strings), and `excludeTaskArgId` (Boolean)                                                                                                                         |
| `namingStrategy`   | String, either `increment` or `uuid` | Determines how the default names are generated for new cells.                                                                                                                      |
| `excludeFromGraph` | Boolean                              | Determines whether to hide instances of the cell from the graph view of your pipeline editor.                                                                                      |
| `returnsRawValue`  | Boolean                              | Indicates whether the custom operator returns a raw value. Set to `true` if the operator uses TaskFlow. If set to false, `.output` is appended to the name of the operator output. |


## Configs JSON reference

The following table is a reference for all possible key-value pairs in the `configs` section of the JSON request.

You can configure multiple `configs` objects for each parameter you want the user to enter. 

| Name               | Type                                 | Description                                                                                                                                                                        |
| ------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`         | String                             | The unique identifier for the parameter.                                                                                                                                      |
| `dataType`    | String, either `string`, `stringList`, `boolean`, `integer`                              | The parameter's value type.                                                              |
| `display`   | Key-value pairs | Determines how the parameter is displayed. See [Display JSON reference](#display-json-reference)                                                                                                                      |
| `excludeFromGraph` | Boolean                              | Determines whether to hide instances of the cell from the graph view of your pipeline editor.                                                                                      |
| `returnsRawValue`  | Boolean                              | Indicates whether the custom operator returns a raw value. Set to `true` if the operator uses TaskFlow. If set to false, `.output` is appended to the name of the operator output. |
| `validity` | Key-value pairs | Configurations to determine which inputs for the parameter are valid. See [Validity JSON reference](#validity-json-reference)|

### Display JSON reference

For each `configs` object, you can configure the following values in a `display` object to change how the parameter appears to users.

| Name               | Type                                 | Description                                                                                                                                                                        |
| ------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `label`         | String                             | The label for the parameter.                                                                                                                                      |
| `description`    | String                              | The description for the parameter.                                                            |
| `default`   | Key-value pair. The key becomes the default `dataType` and the value becomes the default value. | The default type and value for the parameter.                                                                                                                      |
| `example` | Key-value pair. The key becomes the default `dataType` and the value becomes the default value.                              | The example value that appears in placeholder text.                                                                                      |
| `fixedWidthFont`  | Boolean                              | Determines whether to format input as a fixed-width font. |
| `numLines`  | Integer                              | The number of lines to show for the user input. |
| `highlightLanguage`  | String, either `python`, `sql`, or `js`.                              | Determines whether the user's input is formatted with syntax highlighting. |


### Validity JSON reference

For each `configs` object, you can configure the following values in a `validity` object to limit the possible inputs a user can enter for the parameter value.

| Name               | Type                                 | Description                                                                                                                                                                        |
| ------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mandatory`         | Boolean                             | Determines whether the parameter is required.                                                                                                                                      |
| `domain`    | Key-value pair.                              | Limit where the user can select a value from. Set `source` (either `stringList` or `connections`) or `valuesStringList` (List of strings, set only if source is `stringList`) |                                                           |

## Example JSON 

The following configuration is an example of how you can configure a custom operator cell to call an internal API. 

```json
{
  "display": {
    "label": "Call Internal API",
    "description":"A custom cell type to call an internal API"
  },
  "behavior": {
    "runnable": true,
    "generatesData":true,
    "namingStrategy": "increment",
    "excludeFromGraph": false,
    "returnsRawValue": false
  },
  "generation": {
    "type": "invoke",
    "invoke": {
      "functionName": "InternalAPIOperator",
      "imports": [
        "from include.operators.api import InternalAPIOperator"
      ]
    }
  },
  "configs": [
    {
      "key": "endpoint",
      "dataType": "string",
      "display": {
        "label": "Endpoint",
        "description": "The endpoint to hit. Starts with a /"
      },
      "validity": {
        "mandatory": true
      }
    },
    {
      "key": "method",
      "dataType": "string",
      "display": {
        "label": "HTTP Method"
      },
      "validity": {
        "mandatory": true,
        "domain": {
          "source": "stringList",
          "valuesStringList": [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "HEAD",
            "OPTIONS",
            "PATCH"
          ]
        }
      }
    }
  ]
}
```

This is how the cell will render in the pipeline editor:

![How the example cell appears in the Cloud UI](/img/cloud-ide/custom-cell-example.png)