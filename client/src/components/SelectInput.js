import React, { useState } from "react";
import Select from "react-select";

const SelectInput = ({
  label,
  options,
  value,
  setValue,
  showAutocomplete,
  setShowAutocomplete,
  submitClicked,
  required = false,
  isMulti = false,
  formatOptionLabel = null,
  customStyle,
}) => {
  const [touched, setTouched] = useState(false);

  const showWarning = required && submitClicked && !value;
  const style = {
    // prettier-ignore
    border: `1px solid ${ showWarning ? "red" : (showAutocomplete && !touched ? "#00adef" : "lightgrey")}`,
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
      <Select
        styles={{
          container: (provided) => ({
            ...provided,
            width: "100%",
            ...customStyle,
          }),
          control: (provided) => ({
            ...provided,
            boxShadow: "none",
            "&:hover": {},
            ...style,
          }),
        }}
        value={value}
        onChange={(e) => {
          setShowAutocomplete(false);
          setTouched(true);
          setValue(e);
        }}
        options={options}
        formatOptionLabel={formatOptionLabel}
        isMulti={isMulti}
      ></Select>
    </div>
  );
};

export default SelectInput;
