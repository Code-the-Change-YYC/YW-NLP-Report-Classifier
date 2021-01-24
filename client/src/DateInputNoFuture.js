import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

import { Input } from "./App";

export function DateInputNoFuture({ labelText, date, setDate, onChangeCallback = () => {} }) {
  const [invalid, setInvalid] = useState(false);

  return (
    <>
      <label>
        {labelText}{' '}
        {invalid ? <b>Date is in the future, select an earlier time.</b> : ''}
      </label>
      <DatePicker
        selected={date}
        showTimeSelect
        timeIntervals={15}
        style={{ padding: '5px' }}
        customInput={
          <Input style={invalid ? { border: '1px solid red' } : {}}></Input>
        }
        dateFormat='MMMM d, yyyy h:mm aa'
        value={Date.now()}
        onChange={(date) => {
          // date can still be in the future if user types into the input
          // instead of using date picker
          if (date > Date.now()) {
            setDate(null);
            setInvalid(true);
          } else {
            setDate(date);
            setInvalid(false);
          }
          onChangeCallback();
        }}
        maxDate={new Date()}
        minTime={new Date().setHours(0, 0, 0, 0)}
        maxTime={new Date()}
      ></DatePicker>
    </>
  );
}
