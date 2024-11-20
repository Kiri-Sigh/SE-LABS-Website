import React from "react";

/**
 * Recursive function to render an object as nested HTML elements.
 * @param {Object} obj - The object to display.
 * @param {number} level - The current depth of recursion (used for indentation).
 * @returns {JSX.Element[]} - Rendered elements.
 */
const renderDeepObject = (obj, level = 0) => {
  return Object.entries(obj).map(([key, value]) => {
    const isObject = typeof value === "object" && value !== null;

    return (
      <div key={key} style={{ marginLeft: `${level * 20}px` }}>
        <strong>{key}:</strong>{" "}
        {isObject ? (
          renderDeepObject(value, level + 1) // Recursively render nested objects
        ) : (
          <span>{value !== null ? value : "null"}</span> // Render primitive values
        )}
      </div>
    );
  });
};

/**
 * Component to render an object using the renderDeepObject function.
 * @param {Object} props - Component props.
 * @param {Object} props.data - The object to display.
 * @returns {JSX.Element} - Rendered deep object.
 */
const DeepObjectViewer = ({ data }) => {
  return (
    <div>
      <h3>Deep Object Viewer</h3>
      {renderDeepObject(data)}
    </div>
  );
};

export default DeepObjectViewer;
