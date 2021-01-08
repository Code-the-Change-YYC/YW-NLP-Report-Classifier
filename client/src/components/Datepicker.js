import React, { useState } from "react";
import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Input } from "./../styled";

const DatePicker = ({
  label,
  value,
  setValue,
  setShowAutocomplete,
  submitClicked,
  required,
}) => {
  const showWarning = submitClicked && !value;
  const style = {
    width: "95%",
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
      <ReactDatePicker
        selected={value}
        onChange={(date) => {
          setValue(date);
          if (!touched) {
            setShowAutocomplete(false);
          }
          setTouched(true);
        }}
        showTimeSelect
        timeIntervals={15}
        style={{ padding: "5px" }}
        customInput={<Input></Input>}
        dateFormat="MMMM d, yyyy h:mm aa"
      ></ReactDatePicker>
    </div>
  );
};

export default DatePicker;
