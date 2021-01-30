export default {
    name: 'cirForm',
    title: 'Critical Incident Report Form',
    type: 'document',
    fields: [
        {
            name: 'primaryIncTypes',
            title: 'Primary Incident Types',
            description: 'The values for the primary incident type dropdown.',
            type: 'array',
            of: [{ type: 'string' }],
        },
        {
            name: 'locations',
            title: 'Locations',
            description: 'The values for the location dropdown.',
            type: 'array',
            of: [{ type: 'optionWithKeywords' }],
        },
        {
            name: 'programs',
            title: 'Programs',
            description: 'The values for the program dropdown.',
            type: 'array',
            of: [{ type: 'optionWithKeywords' }],
        },
        {
            name: 'immediateResponses',
            title: 'Immediate Responses',
            description: 'The values for the immediate response dropdown.',
            type: 'array',
            of: [{ type: 'optionWithKeywords' }],
        },
        {
            name: 'servicesInvolved',
            title: 'Services Involved',
            description: 'The values for the services involved dropdown.',
            type: 'array',
            of: [{ type: 'optionWithKeywords' }],
        },
        {
            name: 'riskAssessmentTimeframe',
            title: 'Risk Assessment Timeframe',
            description: 'Time frame to be considered in risk assessment in months.',
            type: 'number',
            validation: Rule => Rule.integer().positive()
        }
    ],
}
