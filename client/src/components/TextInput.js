import React, { useState } from "react";
import { Input } from "../styled";

const TextInput = ({
  label,
  value,
  setValue,
  showAutocomplete,
  setShowAutocomplete,
  submitClicked,
  required,
  customStyle,
}) => {
  const [touched, setTouched] = useState(false);

  const showWarning = required && submitClicked && !value;

  const style = {
    width: "100%",
    // prettier will remove the parentheses around the second ternanry if statement:
    // prettier-ignore
    border: `1px solid ${ showWarning ? "red" : (showAutocomplete && !touched ? "#00adef" : "lightgrey")}`,
    ...customStyle,
  };

  return (
    <div style={{ width: "100%" }}>
      <label>
        {label + (required ? " *" : "")}
        <input
          type="checkbox"
          checked={showAutocomplete}
          onClick={() => setShowAutocomplete()}
          style={{ marginLeft: "10px" }}
        />
      </label>
      <Input
        value={value}
        onChange={(e) => {
          setShowAutocomplete(false);
          setTouched(true);
          setValue(e.target.value);
        }}
        style={style}
      ></Input>
    </div>
  );
};

export default TextInput;
