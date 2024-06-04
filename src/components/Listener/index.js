import React, { useState, useEffect } from "react";
import { View, Image, StyleSheet } from "react";
import Konami from "konami";
import styles from "./styles.module.css";

export default function Listener() {
  return useEffect(() => {
    const easterEgg = new Konami(() => {
        return <img
          style={styles.image}
          src="/docs/img/docs/lifestyle.jpg"
          alt="Great job managing your bills. Now try managing my lifestyle. -JW"
        />;
    }, []);
  });
}
