import React, { useState, useCallback, useEffect } from "react";
import logo from "./logo.jpg";
import "./App.css";
import _ from "lodash";
import chrono from "chrono-node";
import Select from "react-select";
import styled from "styled-components";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { getPrediction } from "./actions/predict";

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

  margin: 5px 0px;
`;

const Input = styled.input`
  padding: 8px 5px;
  font-size: 12pt;
  border: 1px solid lightgray;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
`;

function App() {
  // State variables
  const [location, setLocation] = useState(null);
  const [clientInitials, setClientInitials] = useState("");
  const [services, setServices] = useState([]);
  const [incidentType, setIncidentType] = useState("");
  const [date, setDate] = useState(new Date());

  // description does not need a touched variable - only the autocompleted fields
  const [description, setDescription] = useState("");

  // the "Touched" variables keep track of whether or not that form field was edited by the client.
  // If so, then we stop overwriting the client's manual input
  const [locationTouched, setLocationTouched] = useState(false);
  const [clientInitialsTouched, setClientInitialsTouched] = useState(false);
  const [servicesTouched, setServicesTouched] = useState(false);
  const [incidentTypeTouched, setIncidentTypeTouched] = useState(false);
  const [dateTouched, setDateTouched] = useState(false);

  const locationOptions = [
    {
      value: "community",
      label: "In community",
    },
    {
      value: "croydon",
      label: "YW Croydon",
    },
    {
      value: "downtown",
      label: "YW Downtown",
    },
    {
      value: "hub",
      label: "YW Hub",
    },
    {
      value: "maple",
      label: "YW Maple",
    },
    {
      value: "providence",
      label: "YW Croydon",
    },
    {
      value: "sheriff king",
      label: "YW Sheriff King",
    },
  ];

  const serviceOptions = [
    { value: "cps", label: "Child Welfare (CPS)" },
    { value: "ems", label: "EMS" },
    { value: "police", label: "Police" },
    { value: "fire", label: "Fire" },
    { value: "doap/pact", label: "Outreach (DOAP/PACT)" },
  ];

  // Checking functions
  // These functions are run when the description updates and contain the logic
  // for autocompleting the form fields.

  const checkDate = () => {
    const results = chrono.parse(description);

    if (results && results.length) {
      setDate(results[0].start.date());
    }
  };

  const checkServices = () => {
    const lowercasedDescription = description.toLowerCase();
    const newServices = [];
    if (
      lowercasedDescription.includes("cps") ||
      lowercasedDescription.includes("child welfare")
    ) {
      newServices.push({ value: "cps", label: "Child Welfare (CPS)" });
    }
    if (lowercasedDescription.includes("ems")) {
      newServices.push({ value: "ems", label: "EMS" });
    }
    if (lowercasedDescription.includes("police")) {
      newServices.push({ value: "police", label: "Police" });
    }
    if (
      lowercasedDescription.includes("fire services") ||
      lowercasedDescription.includes("fire department") ||
      lowercasedDescription.includes("fire station")
    ) {
      newServices.push({ value: "fire", label: "Fire" });
    }
    if (
      lowercasedDescription.includes("doap") ||
      lowercasedDescription.includes("pact")
    ) {
      newServices.push({ value: "doap/pact", label: "Outreach (DOAP/PACT)" });
    }

    setServices(newServices);
  };

  const checkLocation = () => {
    const lowercasedDescription = description.toLowerCase();

    if (lowercasedDescription.includes("community")) {
      setLocation({ value: "community", label: "In community" });
    } else if (lowercasedDescription.includes("Croydon".toLowerCase())) {
      setLocation({ value: "croydon", label: "YW Croydon" });
    } else if (lowercasedDescription.includes("Downtown".toLowerCase())) {
      setLocation({ value: "downtown", label: "YW Downtown" });
    } else if (lowercasedDescription.includes("Hub".toLowerCase())) {
      setLocation({ value: "hub", label: "YW Hub" });
    } else if (lowercasedDescription.includes("Maple".toLowerCase())) {
      setLocation({ value: "maple", label: "YW Maple" });
    } else if (lowercasedDescription.includes("Providence".toLowerCase())) {
      setLocation({ value: "providence", label: "YW Providence" });
    } else if (
      lowercasedDescription.includes("YW Sheriff King".toLowerCase())
    ) {
      setLocation({ value: "sheriff king", label: "YW Sheriff King" });
    }
  };

  const checkInitials = () => {
    const found = description.match(/[A-Z]{2}/g);
    if (found && found.length) {
      setClientInitials(found[0]);
    }
  };

  const checkIncidentType = async () => {
    const prediction = await getPrediction(description);
    setIncidentType(prediction);
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
      if (!servicesTouched) {
        checkServices();
      }
      if (!dateTouched) {
        checkDate();
      }
      if (!incidentTypeTouched) {
        checkIncidentType();
      }
    }, 1000),
    [checkLocation, checkInitials, checkServices, checkDate, _]
  );

  useEffect(onDescriptionUpdate, [description]);

  return (
    <div className="App">
      <img src={logo} alt="YW logo"></img>
      <h1>Critical Incident Report Form</h1>
      <h2>Prototype - June 30, 2020 </h2>

      <form>
        <FormRow>
          <label>Client Involved</label>
          <Input
            value={clientInitials}
            onChange={(e) => {
              setClientInitials(e.target.value);
              setClientInitialsTouched(true);
            }}
          ></Input>
        </FormRow>
        <FormRow>
          <label>Services Involved</label>
          <Select
            styles={{
              container: (provided) => ({ ...provided, width: "100%" }),
            }}
            value={services}
            isMulti
            onChange={(newSelection) => {
              setServices(newSelection);
              setServicesTouched(true);
            }}
            options={serviceOptions}
          ></Select>
        </FormRow>
        <FormRow>
          <label>Location</label>
          <Select
            styles={{
              container: (provided) => ({ ...provided, width: "100%" }),
            }}
            value={location}
            onChange={(newLocation) => {
              setLocation(newLocation);
              setLocationTouched(true);
            }}
            options={locationOptions}
          ></Select>
        </FormRow>
        <FormRow>
          <label>Date</label>
          <DatePicker
            selected={date}
            onChange={(date) => {
              setDate(date);
              setDateTouched(true);
            }}
            showTimeSelect
            timeIntervals={15}
            style={{ padding: "5px" }}
            customInput={<Input></Input>}
            dateFormat="MMMM d, yyyy h:mm aa"
          ></DatePicker>
        </FormRow>
        <FormRow>
          <label>Incident Type</label>
          <Input
            value={incidentType}
            onChange={(e) => {
              setIncidentType(e.target.value);
              setIncidentTypeTouched(true);
            }}
          ></Input>
        </FormRow>
        <FormRow>
          <label>Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={7}
          ></textarea>
        </FormRow>
      </form>
    </div>
  );
}

export default App;
