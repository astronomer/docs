import React, { useState, useEffect } from "react";
import { View, Image, StyleSheet } from "react";
import Konami from "konami";
import styles from "./styles.module.css";

export default function Listener() {
  useEffect(() => {
    const easterEgg = new Konami(() => {
      document.querySelector('.jw-img').setAttribute('style', 'display:block')
    }, []);
  });

  return (
    <img
      className="jw-img"
      style={{ 'display': 'none' }}
      src="/docs/img/docs/lifestyle.jpg"
      alt="Great job managing your bills. Now try managing my lifestyle. -JW"
      loading="lazy"
    />
  )
}
