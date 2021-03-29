import React, { useState } from "react";
import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Input } from "./../styled";

const DateInput = ({
  label,
  value,
  setValue,
  showAutocomplete,
  setShowAutocomplete,
  submitClicked,
  required,
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
      <ReactDatePicker
        selected={value}
        onChange={(date) => {
          setShowAutocomplete(false);
          setTouched(true);
          setValue(date);
        }}
        showTimeSelect
        timeIntervals={15}
        style={{ padding: "5px" }}
        customInput={<Input style={style}></Input>}
        dateFormat="MMMM d, yyyy h:mm aa"
      ></ReactDatePicker>
    </div>
  );
};

export default DateInput;
