import React from "react";
import SelectInput from "./SelectInput";

const IncTypeOption = ({ confidence, label }) => {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        width: "100%",
      }}
    >
      <div>{label}</div>
      <div style={{ marginLeft: "15px", color: "#999999" }}>{confidence}</div>
    </div>
  );
};

const IncTypePrimaryField = ({
  incidentType,
  setIncidentType,
  setShowAutocomplete,
  sortedIncTypeOptions,
  submitClicked,
}) => {

  const numConfidenceValues = 5;
  const reactSelectIncTypeOpts = sortedIncTypeOptions?.map((opt, i) => {
    if (i > numConfidenceValues - 1) {
      return {
        ...opt,
        confidence: "",
      };
    } else {
      return opt;
    }
  });

  return (
    <SelectInput
      label="Incident Type (Primary)"
      value={incidentType}
      options={reactSelectIncTypeOpts}
      setValue={setIncidentType}
      setShowAutocomplete={setShowAutocomplete}
      submitClicked={submitClicked}
      formatOptionLabel={IncTypeOption}
      required
      customStyle={{width: "95%"}}
    ></SelectInput>
  );
};

export default IncTypePrimaryField;
