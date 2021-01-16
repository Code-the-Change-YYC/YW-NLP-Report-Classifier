import React, { useState } from "react";
import { DateInputNoFuture } from "./DateInputNoFuture";

const DatePicker = ({
  label,
  value,
  setValue,
  setShowAutocomplete,
  required,
}) => {
  const [touched, setTouched] = useState(false);
  const [autoCompleteCheckbox, setAutoCompleteCheckbox] = useState(true);

  const handleClick = (e) => {
    setAutoCompleteCheckbox(!autoCompleteCheckbox);
    setShowAutocomplete();
  };

  return (
    <div style={{ width: "100%" }}>
      <DateInputNoFuture
        date={value}
        setDate={setValue}
        onChangeCallback={() => {
          if (!touched) {
            setShowAutocomplete(false);
          }
          setTouched(true);
        }}
        labelText={label}
      >
        {label + (required ? " *" : "")}
        <input
          type="checkbox"
          checked={autoCompleteCheckbox}
          onClick={handleClick}
          style={{ marginLeft: "10px" }}
        />
      </DateInputNoFuture>
    </div>
  );
};

export default DatePicker;
