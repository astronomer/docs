import React, { useState, useEffect } from 'react';
import { useHistory, useLocation } from '@docusaurus/router';
import styles from './styles.module.css';

export default function SelectNav({ label, items }) {
  let history = useHistory();
  let path = useLocation();

  const [currentVersion, setCurrentVersion] = useState(items[0].label);

  function navigateOnChange(event) {
    setCurrentVersion(event.target.querySelector(`option[value='${event.target.value}']`).text);
    history.push(event.target.value);
  };

  useEffect(() => {
    document.querySelector(`option[value*='${path.pathname}']`) && setCurrentVersion(document.querySelector(`option[value*='${path.pathname}']`).text);
  }, [currentVersion]);

  return (
    <div className={styles.selectNav} id="selectNav">
      {label && (
        <label htmlFor="selectNav" className={styles.selectNav__label}>
          {label}
        </label>
      )}
      <select id="selectNav" name="selectNav" className={styles.selectNav__select} onChange={navigateOnChange} placeholer={currentVersion} value={currentVersion}>
        <option>{currentVersion} </option>
        {items.map((item, i) => (
          <option key={i} className={styles.selectNav__option} value={item.to} hidden={currentVersion.indexOf(item.label) > -1}>{item.label}</option>
        ))}
      </select>
    </div>
  )
}