import { useState } from "react";

const useTextFieldInfo = () => {
  const [userValue, setUserValue] = useState("");
  const [autocompleteValue, setAutocompleteValue] = useState("");
  const [useAutocomplete, setUseAutocompleteDefault] = useState(true);
  const valid = useAutocomplete ? autocompleteValue.length > 0 : userValue.length > 0;
  const value = useAutocomplete ? autocompleteValue : userValue;

  function setUseAutocomplete(newValue) {
    // if no argument, toggle
    if (newValue === undefined) {
      setUseAutocompleteDefault(!useAutocomplete);
      return;
    }

    setUseAutocompleteDefault(newValue);
  }

  return [value, setUserValue, setAutocompleteValue, setUseAutocomplete, valid];
}

export default useTextFieldInfo;