import React, { useState, useCallback, useEffect } from "react";
import logo from "./logo.jpg";
import "./App.css";
import _ from "lodash";
import chrono from "chrono-node";
import Select from "react-select";
import styled from "styled-components";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

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

function App() {
  // State variables
  const [location, setLocation] = useState(null);
  const [clientInitials, setClientInitials] = useState("");
  const [services, setServices] = useState([]);
  const [incidentTypePri, setIncidentTypePri] = useState(null);
  const [incidentTypeSec, setIncidentTypeSec] = useState(null);
  const [date, setDate] = useState(new Date());
  //
  const [clientSecInitials, setClientSecInitials] = useState("");
  const [locationDetail, setLocationDetail] = useState("");
  const [staffInvolvedFirst, setStaffInvolvedFirst] = useState("");
  const [staffInvolvedLast, setStaffInvolvedLast] = useState("");
  const [program, setProgram] = useState(null);
  const [otherServices, setOtherServices] = useState("");
  const [immediateResponse, setImmediateResponse] = useState(null);
  const [staffCompleting, setStaffCompleting] = useState("");
  const [supervisorReviewer, setSupervisorReviewer] = useState("");
  const [dateCompleted, setDateCompleted] = useState("");

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

  const programOptions = [
    {
      label: "Child Care (Hub)",
      value: "child care hub",
    },
    {
      label: "Child Support",
      value: "child support",
    },
    {
      label: "Compass",
      value: "compass",
    },
    {
      label: "Counselling and Personal Development",
      value: "counselling",
    },
    {
      label: "Croydon (Community Housing)",
      value: "croydon",
    },
    {
      label: "DCRT",
      value: "DCRT",
    },
    {
      label: "Drop-In Child Care",
      value: "croydon",
    },
    {
      label: "Employment Resource Center",
      value: "employment resource center",
    },
  ];

  const incidentTypes = [
    {
      label: "Child abandonment",
      value: "child abandonment",
    },
    {
      label: "Client aggression towards another person",
      value: "client aggression towards another person",
    },
    {
      label: "Client aggression towards property",
      value: "client aggression towards property",
    },
    {
      label: "Client death (offsite)",
      value: "client death (offsite)",
    },
    {
      label: "Client death (onsite)",
      value: "client death (onsite)",
    },
    {
      label: "Client missing",
      value: "client missing",
    },
    {
      label: "Concern for welfare of a child",
      value: "concern for welfare of a child",
    },
    {
      label: "COVID-19 Confirmed",
      value: "COVID-19 confirmed",
    },
    {
      label: "Exposure",
      value: "exposure",
    },
  ];

  const immediateResponses = [
    {
      label: "Called Child Welfare",
      value: "called child welfare",
    },
    {
      label: "Evacution",
      value: "evacution",
    },
    {
      label: "First-aid provided",
      value: "first-aid provided",
    },
    {
      label: "Mental health assessment",
      value: "mental health assessment",
    },
    {
      label: "Naloxone administered",
      value: "naloxone administered",
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
            <label>Services Involved</label>
            <Select
              styles={{
                container: (provided) => ({ ...provided, width: "95%" }),
              }}
              value={services}
              isMulti
              onChange={(newSelection) => {
                setServices(newSelection);
                setServicesTouched(true);
              }}
              options={serviceOptions}
            ></Select>
          </div>
          <div style={{ width: "100%" }}>
            <label>Other Services Involved (if other)</label>
            <Input
              value={otherServices}
              onChange={(e) => setOtherServices(e.target.value)}
            ></Input>
          </div>
        </FormRow>

        <FormRow style={{ flexDirection: "row" }}>
          <div style={{ width: "100%" }}>
            <label>Location</label>
            <Select
              styles={{
                container: (provided) => ({ ...provided, width: "95%" }),
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
            <label>Incident Type (Primary)</label>
            <Select
              styles={{
                container: (provided) => ({ ...provided, width: "95%" }),
              }}
              value={incidentTypePri}
              onChange={(incidentType) => {
                setIncidentTypePri(incidentType);
                setIncidentTypeTouched(true);
              }}
              options={incidentTypes}
            ></Select>
          </div>
          <div style={{ width: "100%" }}>
            <label>Incidept Type (Secondary)</label>
            <Select
              styles={{
                container: (provided) => ({ ...provided, width: "95%" }),
              }}
              value={incidentTypeSec}
              onChange={(incidentType) => {
                setIncidentTypeSec(incidentType);
              }}
              options={incidentTypes}
            ></Select>
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
          <label>Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={7}
          ></textarea>
        </FormRow>
        <FormRow>
          <label>Program</label>
          <Select
            styles={{
              container: (provided) => ({ ...provided, width: "100%" }),
            }}
            value={program}
            onChange={(program) => {
              setProgram(program);
            }}
            options={programOptions}
          ></Select>
        </FormRow>
        <FormRow>
          <label>Immediate Response</label>
          <Select
            styles={{
              container: (provided) => ({ ...provided, width: "100%" }),
            }}
            value={immediateResponse}
            isMulti
            onChange={(newSelection) => setImmediateResponse(newSelection)}
            options={immediateResponses}
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
            selected={date}
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
      </form>
    </div>
  );
}

export default App;
