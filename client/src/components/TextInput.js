import React, { useState } from "react";
import { Input } from "../styled";

const TextInput = ({
  label,
  value,
  setValue,
  setShowAutocomplete,
  submitClicked,
  required
}) => {
  const showWarning = submitClicked && !value;
  const style = { width: "95%", border: `1px solid${showWarning ? " red" : ""}` };
  const [touched, setTouched] = useState(false);

  const handleClick = (e) => {
    e.preventDefault();
    setShowAutocomplete();
  }

  return (
    <div style={{ width: "100%" }}>
      <label>{label + (required ? " *" : "")}<button onClick={handleClick}>T</button></label>
      <Input
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
          if (!touched) {
            setShowAutocomplete(false);
          }
          setTouched(true);
        }}
        style={style}
      ></Input>
    </div>
  );
};

export default TextInput;
