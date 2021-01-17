import React, { useState } from "react";
import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Input } from "./../styled";

const DateInput = ({
  label,
  value,
  setValue,
  setShowAutocomplete,
  submitClicked,
  required,
  noFutureDate = false,
}) => {
  const [touched, setTouched] = useState(false);
  const [autoCompleteCheckbox, setAutoCompleteCheckbox] = useState(true);

  const handleClick = (e) => {
    setAutoCompleteCheckbox(!autoCompleteCheckbox);
    setShowAutocomplete();
  };

  const showWarning = submitClicked && !value;
  const style = {
    // prettier-ignore
    border: `1px solid ${ showWarning ? "red" : (autoCompleteCheckbox && !touched ? "#00adef" : "lightgrey")}`,
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
          if (noFutureDate && date > Date.now()) {
            setValue(new Date());
          } else {
            setValue(date);
          }
          if (!touched) {
            setShowAutocomplete(false);
          }
          setTouched(true);
        }}
        showTimeSelect
        timeIntervals={15}
        style={{ padding: "5px" }}
        customInput={<Input style={style}></Input>}
        dateFormat="MMMM d, yyyy h:mm aa"
        maxDate={noFutureDate ? new Date() : null}
        minTime={noFutureDate ? new Date().setHours(0, 0, 0, 0) : null}
        maxTime={noFutureDate ? new Date() : null}
      ></ReactDatePicker>
    </div>
  );
};

export default DateInput;
