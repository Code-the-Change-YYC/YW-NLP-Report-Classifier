import React, { useState, useCallback, useEffect } from "react";
import logo from "./logo.jpg";
import "./App.css";
import _ from "lodash";
import chrono from "chrono-node";
import styled from "styled-components";

const FormRow = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  & > input,
  textarea {
    align-self: stretch;
    margin-top: 5px;
  }

  margin: 5px 0px;
`;

function App() {
  const [location, setLocation] = useState("");
  const [locationTouched, setLocationTouched] = useState(false);
  const [clientInitials, setClientInitials] = useState("");
  const [clientInitialsTouched, setClientInitialsTouched] = useState(false);
  const [services, setServices] = useState("");
  const [servicesTouched, setServicesTouched] = useState(false);
  const [incidentType, setIncidentType] = useState("");
  const [incidentTypeTouched, setIncidentTypeTouched] = useState(false);
  const [date, setDate] = useState("");
  const [dateTouched, setDateTouched] = useState(false);
  const [description, setDescription] = useState("");

  const checkDate = () => {
    const results = chrono.parse(description);

    if (results && results.length) {
      setDate(results[0].start.date());
    }
  };

  const checkServices = () => {
    const lowercasedDescription = description.toLowerCase();
    if (
      lowercasedDescription.includes("cps") ||
      lowercasedDescription.includes("child welfare")
    ) {
      setServices("Child Welfare (CFS)");
    } else if (lowercasedDescription.includes("ems")) {
      setServices("EMS");
    } else if (lowercasedDescription.includes("police")) {
      setServices("police");
    } else if (
      lowercasedDescription.includes("fire services") ||
      lowercasedDescription.includes("fire department")
    ) {
      setServices("Fire");
    } else if (
      lowercasedDescription.includes("doap") ||
      lowercasedDescription.includes("pact")
    ) {
      setServices("Outreach (DOAP/PACT)");
    }
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
    [checkLocation, checkInitials, checkServices, _]
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
          <input
            value={services}
            onChange={(e) => {
              setServices(e.target.value);
              setServicesTouched(true);
            }}
          ></input>
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
