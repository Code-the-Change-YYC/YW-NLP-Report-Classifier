import React, { useState, useCallback, useEffect } from "react";
import logo from "./logo.jpg";
import "./App.css";
import _ from "lodash";
import chrono from "chrono-node";
import Select from "react-select";
import styled from "styled-components";

const FormRow = styled.div`
  display: flex;
  flex-direction: column;
  align-items: stretch;

  & > input,
  textarea {
    align-self: stretch;
    margin-top: 5px;
  }

  margin: 5px 0px;
`;

function App() {
  // State variables
  const [location, setLocation] = useState("");
  const [clientInitials, setClientInitials] = useState("");
  const [services, setServices] = useState([]);
  const [incidentType, setIncidentType] = useState("");
  const [date, setDate] = useState("");

  // description does not need a touched variable - only the autocompleted fields
  const [description, setDescription] = useState("");

  // the "Touched" variables keep track of whether or not that form field was edited by the client.
  // If so, then we stop overwriting the client's manual input
  const [locationTouched, setLocationTouched] = useState(false);
  const [clientInitialsTouched, setClientInitialsTouched] = useState(false);
  const [servicesTouched, setServicesTouched] = useState(false);
  const [incidentTypeTouched, setIncidentTypeTouched] = useState(false);
  const [dateTouched, setDateTouched] = useState(false);

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
      setLocation("In community");
    } else if (lowercasedDescription.includes("Croydon".toLowerCase())) {
      setLocation("YW Croydon");
    } else if (lowercasedDescription.includes("Downtown".toLowerCase())) {
      setLocation("YW Downtown");
    } else if (lowercasedDescription.includes("Hub".toLowerCase())) {
      setLocation("YW Hub");
    } else if (lowercasedDescription.includes("Maple".toLowerCase())) {
      setLocation("YW Maple");
    } else if (lowercasedDescription.includes("Providence".toLowerCase())) {
      setLocation("YW Providence");
    } else if (
      lowercasedDescription.includes("YW Sheriff King".toLowerCase())
    ) {
      setLocation("YW Sheriff King");
    }
  };

  const checkInitials = () => {
    const found = description.match(/[A-Z]{2}/g);
    if (found && found.length) {
      setClientInitials(found[0]);
    }
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
          <input
            value={clientInitials}
            onChange={(e) => {
              setClientInitials(e.target.value);
              setClientInitialsTouched(true);
            }}
          ></input>
        </FormRow>
        <FormRow>
          <label>Services Involved</label>
          <Select
            value={services}
            isMulti
            onChange={(newSelection) => {
              setServices(newSelection);
              setServicesTouched(true);
            }}
            options={[
              { value: "cps", label: "Child Welfare (CPS)" },
              { value: "ems", label: "EMS" },
              { value: "police", label: "Police" },
              { value: "fire", label: "Fire" },
              { value: "doap/pact", label: "Outreach (DOAP/PACT)" },
            ]}
          ></Select>
        </FormRow>
        <FormRow>
          <label>Location</label>
          <input
            value={location}
            onChange={(e) => {
              setLocation(e.target.value);
              setLocationTouched(true);
            }}
          ></input>
        </FormRow>
        <FormRow>
          <label>Date</label>
          <input
            value={date}
            onChange={(e) => {
              setDate(e.target.value);
              setDateTouched(true);
            }}
          ></input>
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
