import React, { useState } from "react";
import { Input } from "../styled";

const TextInput = ({
  label,
  value,
  setValue,
  setShowAutocomplete,
  submitClicked,
  required,
  customStyle,
}) => {
  const [touched, setTouched] = useState(false);
  const [autoCompleteCheckbox, setAutoCompleteCheckbox] = useState(true);

  const toggleCheckbox = (e) => {
    setAutoCompleteCheckbox(!autoCompleteCheckbox);
    setShowAutocomplete();
  };

  const showWarning = submitClicked && !value;

  const style = {
    width: "100%",
    // prettier will remove the parentheses around the second ternanry if statement:
    // prettier-ignore
    border: `1px solid ${ showWarning ? "red" : (autoCompleteCheckbox && !touched ? "#00adef" : "lightgrey")}`,
    ...customStyle,
  };

  return (
    <div style={{ width: "100%" }}>
      <label>
        {label + (required ? " *" : "")}
        <input
          type="checkbox"
          checked={autoCompleteCheckbox}
          onClick={toggleCheckbox}
          style={{ marginLeft: "10px" }}
        />
      </label>
      <Input
        value={value}
        onChange={(e) => {
          setShowAutocomplete(false);
          setAutoCompleteCheckbox(false);
          setTouched(true);
          setValue(e.target.value);
        }}
        style={style}
      ></Input>
    </div>
  );
};

export default TextInput;
