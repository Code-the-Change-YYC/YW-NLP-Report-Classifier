export default {
  name: "cirForm",
  title: "Critical Incident Report Form",
  type: "document",
  fields: [
    {
      name: "primaryIncTypes",
      title: "Primary Incident Types",
      description: "The values for the primary incident type dropdown.",
      type: "array",
      of: [{ type: "optionWithRisk" }],
    },
    {
      name: "locations",
      title: "Locations",
      description: "The values for the location dropdown.",
      type: "array",
      of: [{ type: "optionWithKeywords" }],
    },
    {
      name: "programs",
      title: "Programs",
      description: "The values for the program dropdown.",
      type: "array",
      of: [{ type: "optionWithKeywordsAndRisk" }],
    },
    {
      name: "immediateResponses",
      title: "Immediate Responses",
      description: "The values for the immediate response dropdown.",
      type: "array",
      of: [{ type: "optionWithKeywordsAndRisk" }],
    },
    {
      name: "servicesInvolved",
      title: "Services Involved",
      description: "The values for the services involved dropdown.",
      type: "array",
      of: [{ type: "optionWithKeywordsAndRisk" }],
    },
    {
      name: "childInvolved",
      title: "Child Involved",
      description: "The values for the services involved dropdown.",
      type: "array",
      of: [{ type: "optionWithKeywords" }],
    },
    {
      name: "guestInvolved",
      title: "Non-client Guest Involved",
      description: "The values for the services involved dropdown.",
      type: "array",
      of: [{ type: "optionWithKeywords" }],
    },
    {
      name: "riskAssessmentTimeframe",
      title: "Risk Assessment Timeframe",
      description: "Time frame to be considered in risk assessment in months.",
      type: "number",
      validation: (Rule) => Rule.integer().positive(),
    },
    {
      name: "minimumEmailRiskScore",
      title: "Minimum Risk Score to send an Email",
      description:
        "The minimum assessed risk score for an incident in order to send an email notifcation",
      type: "string",
      options: {
        list: [
          { title: "Low", value: "low" },
          { title: "Medium", value: "medium" },
          { title: "High", value: "high" },
        ],
        layout: "radio",
      },
    },
  ],
};
