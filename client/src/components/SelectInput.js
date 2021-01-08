import React, { useState } from "react";
import Select from "react-select";

const SelectInput = ({
  label,
  options,
  value,
  setValue,
  setShowAutocomplete,
  submitClicked,
  required = false,
  isMulti = false,
  formatOptionLabel = null,
  customStyle,
}) => {
  const showWarning = submitClicked && !value;
  const style = {
    border: `1px solid${showWarning ? " red" : "lightgray"}`,
  };
  const [touched, setTouched] = useState(false);
  const [autoCompleteCheckbox, setAutoCompleteCheckbox] = useState(true);

  const handleClick = (e) => {
    setAutoCompleteCheckbox(!autoCompleteCheckbox);
    setShowAutocomplete();
  };
  return (
    <div style={{ width: "100%" }}>
      <label>
        {label + (required ? " *" : "")}
        <input
          type="checkbox"
          checked={autoCompleteCheckbox}
          onClick={handleClick}
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
          setValue(e);
          if (!touched) {
            setShowAutocomplete(false);
          }
          setTouched(true);
        }}
        options={options}
        formatOptionLabel={formatOptionLabel}
        isMulti={isMulti}
      ></Select>
    </div>
  );

  // return (
  //   <div style={{ width: "100%" }}>
  //     <label>
  //       {label + (required ? " *" : "")}
  //       <input
  //         type="checkbox"
  //         checked={autoCompleteCheckbox}
  //         onClick={handleClick}
  //       />
  //     </label>
  //     <Input
  //       value={value}
  //       onChange={(e) => {
  //         setValue(e.target.value);
  //         if (!touched) {
  //           setShowAutocomplete(false);
  //         }
  //         setTouched(true);
  //       }}
  //       style={style}
  //     ></Input>
  //   </div>
  // );
};

export default SelectInput;
