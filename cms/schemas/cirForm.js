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
    ],
}
