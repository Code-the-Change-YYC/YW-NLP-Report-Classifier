import React, { useState, useCallback, useEffect } from "react";
import logo from "./logo.jpg";
import "./App.css";
import _ from "lodash";
import chrono from "chrono-node";
import Select from "react-select";
import styled from "styled-components";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { getMultiPrediction } from "./actions/predict";
import {
  locationOptions,
  programOptions,
  incidentTypes,
  immediateResponseOptions,
  serviceOptions,
} from "./formOptions";

const FormRow = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  textarea {
    align-self: stretch;
    font-size: 12pt;
  }

  & > label {
    margin-bottom: 5px;
  }

  & > div > label {
    display: flex;
    margin-bottom: 5px;
  }

  margin: 5px 0px;
  text-align: left;
`;

const Input = styled.input`
  padding: 8px 5px;
  font-size: 12pt;
  border: 1px solid lightgray;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
`;

const Textarea = styled.textarea`
  padding: 8px 5px;
  font-size: 12pt;
  border: 1px solid lightgray;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
`;

const HR = styled.hr`
  margin: 20px 30px 20px;
`;

const ModalClose = styled.div`
  float: right;
  text-align: right;
  cursor: pointer;
  line-height: 10px;

  &:before {
    content: "x";
    color: #ff0000;
    font-weight: normal;
    font-family: Arial, sans-serif;
    font-size: 30px;
  }
`;

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

function App() {
  // State variables
  const [location, setLocation] = useState(null);
  const [clientInitials, setClientInitials] = useState("");
  const [servicesInvolved, setservicesInvolved] = useState([]);
  const [incidentTypePri, setIncidentTypePri] = useState(null);
  const [incidentTypeSec, setIncidentTypeSec] = useState({});
  const [dateOccurred, setDateOccurred] = useState(new Date());
  const [clientSecInitials, setClientSecInitials] = useState("");
  const [locationDetail, setLocationDetail] = useState("");
  const [staffInvolvedFirst, setStaffInvolvedFirst] = useState("");
  const [staffInvolvedLast, setStaffInvolvedLast] = useState("");
  const [involvesChild, setInvolvesChild] = useState(null);
  const [involvesNonClient, setInvolvesNonClient] = useState(null);
  const [program, setProgram] = useState(null);
  const [otherServices, setOtherServices] = useState("");
  const [immediateResponse, setImmediateResponse] = useState([]);
  const [staffCompleting, setStaffCompleting] = useState("");
  const [supervisorReviewer, setSupervisorReviewer] = useState("");
  const [dateCompleted, setDateCompleted] = useState(new Date());
  const [description, setDescription] = useState("");
  const [otherSecIncidentType, setOtherSecIncidentType] = useState("");
  const [modalDisplay, setModalDisplay] = useState("none");

  // the "Touched" variables keep track of whether or not that form field was edited by the client.
  // If so, then we stop overwriting the client's manual input
  const [locationTouched, setLocationTouched] = useState(false);
  const [clientInitialsTouched, setClientInitialsTouched] = useState(false);
  const [clientSecInitialsTouched, setClientSecInitialsTouched] = useState(
    false
  );
  const [servicesTouched, setServicesTouched] = useState(false);
  const [incidentTypeTouched, setIncidentTypeTouched] = useState(false);
  const [programTouched, setProgramTouched] = useState(false);
  const [immediateResponseTouched, setImmediateResponseTouched] = useState(
    false
  );
  const [dateTouched, setDateTouched] = useState(false);
  const [incTypesOptions, setIncTypesOptions] = useState(incidentTypes);

  // Checking functions
  // These functions are run when the description updates and contain the logic
  // for autocompleting the form fields.

  const autocompleteSingleOption = (options) => {
    const lowercasedDescription = description.toLowerCase();
    return options.find((option) =>
      (option.keywords || []).some((keyword) =>
        lowercasedDescription.includes(keyword.toLowerCase())
      )
    );
  };

  const autocompleteMultipleOptions = (options) => {
    const lowercasedDescription = description.toLowerCase();
    const newOptions = options.filter((option) =>
      (option.keywords || []).some((keyword) =>
        lowercasedDescription.includes(keyword.toLowerCase())
      )
    );
    return newOptions;
  };

  const checkServices = () =>
    setservicesInvolved(autocompleteMultipleOptions(serviceOptions));

  const checkLocation = () =>
    setLocation(autocompleteSingleOption(locationOptions));

  const checkProgram = () =>
    setProgram(autocompleteSingleOption(programOptions));

  const checkImmediateResponse = () =>
    setImmediateResponse(autocompleteMultipleOptions(immediateResponseOptions));

  const checkDate = () => {
    const results = chrono.parse(description);

    if (results && results.length) {
      setDateOccurred(results[0].start.date());
    }
  };

  const checkInitials = () => {
    const found = description.match(/\b(?!AM|PM)([A-Z]{2})\b/g);
    if (found && found.length) {
      setClientInitials(found[0]);
    } else {
      setClientInitials("");
    }
  };

  const checkSecondInitials = () => {
    const found = description.match(/\b(?!AM|PM)([A-Z]{2})\b/g);
    if (found && found.length) {
      for (const match of found) {
        if (match !== clientInitials) {
          setClientSecInitials(match);
          return;
        }
      }
    }
    setClientSecInitials("");
  };

  const checkIncidentType = async () => {
    const predictions = await getMultiPrediction(description);
    setIncTypesOptions(predictions);
    setIncidentTypePri(predictions[0]);
  };

  // run this 1000 seconds when the description is updated
  const onDescriptionUpdate = useCallback(
    _.throttle(() => {
      if (!locationTouched) {
        checkLocation();
      }
      if (!clientInitialsTouched) {
        checkInitials();
      }
      if (!clientSecInitialsTouched) {
        checkSecondInitials();
      }
      if (!servicesTouched) {
        checkServices();
      }
      if (!dateTouched) {
        checkDate();
      }
      if (!incidentTypeTouched) {
        checkIncidentType();
      }
      if (!programTouched) {
        checkProgram();
      }
      if (!immediateResponseTouched) {
        checkImmediateResponse();
      }
    }, 1000),
    [checkLocation, checkInitials, checkServices, checkDate, _]
  );

  useEffect(onDescriptionUpdate, [description]);

  const handleSubmit = async function (e) {
    e.preventDefault();
    window.open(
      "https://docs.google.com/forms/d/e/1FAIpQLScfxUsVQDwfXkUeVqfHQrhJpUv9_COL6_9bxgXEAL3M_NA5og/viewform?usp=sf_link"
    );
    setModalDisplay("block");
    const formData = {
      location,
      clientInitials,
      // ...
    };
    await fetch("http://localhost:3002/submitForm", {
      mode: "no-cors", // no-cors, *cors, same-origin
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((body) => {
        console.log(body);
      });
  };

  return (
    <div className="App">
      <div
        style={{
          position: "fixed",
          top: "0",
          left: "0",
          width: "100%",
          bottom: "0",
          backgroundColor: "rgba(0,0,0,0.5)",
          zIndex: "10",
          display: modalDisplay, // modalDisplay
        }}
      >
        <div
          className="ModalBox"
          style={{
            width: "500px",
            height: "auto",
            backgroundColor: "#fff",
            float: "none",
            margin: "10% auto 0",
            borderRadius: "7px",
            textAlign: "left",
            padding: "20px",
          }}
        >
          <ModalClose onClick={() => setModalDisplay("none")}></ModalClose>
          <div>
            <b>Client Involved - Primary: </b> {clientInitials}
          </div>
          <div>
            <b>Client Involved - Secondary: </b> {clientSecInitials}
          </div>
          <div>
            <b>Location: </b> {location?.label}
          </div>
          <div>
            <b>Location Detail: </b> {locationDetail}
          </div>
          <div>
            <b>Date of Occurrence: </b> {dateOccurred.toLocaleString()}
          </div>
          <div>
            <b>Services Involved: </b>
            {servicesInvolved?.map((o) => o.label).join(", ")}
          </div>
          <div>
            <b>Other Services Involved: </b> {otherServices}
          </div>
          <div>
            <b>Staff Involved: </b>
            {`${staffInvolvedFirst} ${staffInvolvedLast}`}
          </div>
          <div>
            <b>Incident Type - Primary: </b> {incidentTypePri?.label}
          </div>
          <div>
            <b>Incident Type - Secondary: </b> {incidentTypeSec?.label}
          </div>

          <div>
            <b>Immediate Response: </b>{" "}
            {immediateResponse?.map((o) => o.label).join(", ")}
          </div>

          <div>
            <b>Program: </b> {program?.label}
          </div>

          <div>
            <b>Involves a Child? </b> {involvesChild?.label}
          </div>
          <div>
            <b>Involves a non-client guest? </b> {involvesNonClient?.label}
          </div>

          <div>
            <b>Staff Completing this Report: </b> {staffCompleting}
          </div>
          <div>
            <b>Program Supervisor Reviewer: </b> {supervisorReviewer}
          </div>

          <div style={{ width: "100%", textAlign: "center" }}>
            <input type="submit" value="Submit" onClick={handleSubmit}></input>
          </div>
        </div>
      </div>
      <img src={logo} alt="YW logo"></img>
      <h1>Critical Incident Report Form</h1>
      <h2>Prototype - June 30, 2020 </h2>
      <FormRow>
        <label>Description of Incident</label>
        <Textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={7}
        ></Textarea>
      </FormRow>
      <HR></HR>
      <form>
        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Client Involved - Primary (Initials)</label>
            <Input
              value={clientInitials}
              onChange={(e) => {
                setClientInitials(e.target.value);
                setClientInitialsTouched(true);
              }}
              style={{ width: "95%" }}
            ></Input>
          </div>
          <div style={{ width: "100%" }}>
            <label>Client Involved - Secondary (Initials)</label>
            <Input
              value={clientSecInitials}
              onChange={(e) => setClientSecInitials(e.target.value)}
            ></Input>
          </div>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Location</label>
            <Select
              styles={{
                container: (provided) => ({
                  ...provided,
                  width: "95%",
                }),
              }}
              value={location}
              onChange={(newLocation) => {
                setLocation(newLocation);
                setLocationTouched(true);
              }}
              options={locationOptions}
            ></Select>
          </div>
          <div style={{ width: "100%" }}>
            <label>Location Detail</label>
            <Input
              value={locationDetail}
              onChange={(e) => setLocationDetail(e.target.value)}
            ></Input>
          </div>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Services Involved</label>
            <Select
              styles={{
                container: (provided) => ({
                  ...provided,
                  width: "95%",
                }),
              }}
              value={servicesInvolved}
              isMulti
              onChange={(newSelection) => {
                setservicesInvolved(newSelection);
                setServicesTouched(true);
              }}
              options={serviceOptions}
            ></Select>
          </div>
          <div style={{ width: "100%" }}>
            <label
              style={
                (servicesInvolved || []).some((s) => s.value === "other")
                  ? { fontWeight: "bold" }
                  : {}
              }
            >
              Other Services Involved (if other)
            </label>
            <Input
              value={otherServices}
              onChange={(e) => setOtherServices(e.target.value)}
            ></Input>
          </div>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Primary Staff Involved First Name</label>
            <Input
              value={staffInvolvedFirst}
              onChange={(e) => setStaffInvolvedFirst(e.target.value)}
              style={{ width: "95%" }}
            ></Input>
          </div>
          <div style={{ width: "100%" }}>
            <label>Primary Staff Involved Last Name</label>
            <Input
              value={staffInvolvedLast}
              onChange={(e) => setStaffInvolvedLast(e.target.value)}
            ></Input>
          </div>
        </FormRow>

        <FormRow>
          <label>Date and Time of Occurrence</label>
          <DatePicker
            selected={dateOccurred}
            onChange={(date) => {
              setDateOccurred(date);
              setDateTouched(true);
            }}
            showTimeSelect
            timeIntervals={15}
            style={{ padding: "5px" }}
            customInput={<Input></Input>}
            dateFormat="MMMM d, yyyy h:mm aa"
          ></DatePicker>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <div>
              <label>Incident Type (Primary)</label>
            </div>
            <Select
              formatOptionLabel={IncTypeOption}
              styles={{
                container: (provided) => ({
                  ...provided,
                  width: "95%",
                }),
              }}
              value={incidentTypePri}
              onChange={(incidentType) => {
                setIncidentTypePri(incidentType);
                setIncidentTypeTouched(true);
              }}
              options={incTypesOptions.sort((i) => i.confidence)}
            ></Select>
          </div>
          <div style={{ width: "100%" }}>
            <label>Incident Type (Secondary)</label>
            <Select
              value={incidentTypeSec}
              onChange={(incidentType) => {
                setIncidentTypeSec(incidentType);
              }}
              options={incidentTypes}
            ></Select>
          </div>
        </FormRow>
        <FormRow
          style={{
            display:
              incidentTypeSec && incidentTypeSec.value === "other"
                ? "flex"
                : "none",
            flexDirection: "row",
          }}
        >
          <div style={{ width: "100%" }}></div>
          <div style={{ width: "100%" }}>
            <label>Secondary Incident Type</label>
            <Input
              value={otherSecIncidentType}
              onChange={(e) => setOtherSecIncidentType(e.target.value)}
            ></Input>
          </div>
        </FormRow>
        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Did this incident involve a child?</label>
            <Select
              styles={{
                container: (provided) => ({
                  ...provided,
                  width: "95%",
                }),
              }}
              value={involvesChild}
              onChange={(option) => {
                setInvolvesChild(option);
              }}
              options={[
                { value: "no", label: "No" },
                { value: "yes", label: "Yes" },
              ]}
            ></Select>
          </div>
          <div style={{ width: "100%" }}>
            <label>Did this incident involve a non-client guest?</label>
            <Select
              value={involvesNonClient}
              onChange={(option) => {
                setInvolvesNonClient(option);
              }}
              options={[
                { value: "no", label: "No" },
                { value: "yes", label: "Yes" },
              ]}
            ></Select>
          </div>
        </FormRow>

        <FormRow>
          <label>Program</label>
          <Select
            styles={{
              container: (provided) => ({
                ...provided,
                width: "100%",
              }),
            }}
            value={program}
            onChange={(program) => {
              setProgram(program);
              setProgramTouched(true);
            }}
            options={programOptions}
          ></Select>
        </FormRow>
        <FormRow>
          <label>Immediate Response to the Incident</label>
          <Select
            styles={{
              container: (provided) => ({
                ...provided,
                width: "100%",
              }),
            }}
            value={immediateResponse}
            isMulti
            onChange={(newSelection) => {
              setImmediateResponse(newSelection);
              setImmediateResponseTouched(true);
            }}
            options={immediateResponseOptions}
          ></Select>
        </FormRow>
        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Name of Staff Completing this Report</label>
            <Input
              value={staffCompleting}
              onChange={(e) => setStaffCompleting(e.target.value)}
              style={{ width: "95%" }}
            ></Input>
          </div>
          <div style={{ width: "100%" }}>
            <label>Name of Program Supervisor Reviewer</label>
            <Input
              value={supervisorReviewer}
              onChange={(e) => setSupervisorReviewer(e.target.value)}
            ></Input>
          </div>
        </FormRow>
        <FormRow>
          <label>Completed On</label>
          <DatePicker
            selected={dateCompleted}
            showTimeSelect
            timeIntervals={15}
            style={{ padding: "5px" }}
            customInput={<Input></Input>}
            dateFormat="MMMM d, yyyy h:mm aa"
            value={Date.now()}
            onChange={(date) => {
              setDateCompleted(date);
            }}
          ></DatePicker>
        </FormRow>
        <input
          type="submit"
          value="Next"
          onClick={(e) => {
            e.preventDefault();
            setModalDisplay("block");
          }}
        ></input>
        <button onClick={(e) => e.preventDefault()}>Download</button>
      </form>
    </div>
  );
}

export default App;
