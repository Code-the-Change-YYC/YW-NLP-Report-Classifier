import React, { useState } from "react";
import { Input } from "../styled";

const TextInput = ({
  label,
  info,
  setValue,
  setShowAutocomplete,
  submitClicked,
  required
}) => {
  const showWarning = submitClicked && !info.value;
  const style = { width: "95%", border: `1px solid${showWarning ? " red" : ""}` };
  const [touched, setTouched] = useState(false);

  const valueToShow = info.showAutocomplete ? info.autocomplete : info.manual;

  return (
    <div style={{ width: "100%" }}>
      <label>{label + (required ? " *" : "")}<button>T</button></label>
      <Input
        value={valueToShow}
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
