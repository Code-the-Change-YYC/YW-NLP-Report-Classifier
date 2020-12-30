export default {
    name: 'optionWithKeywords',
    type: 'object',
    fields: [
        {
            name: 'name',
            title: 'Option Name',
            description: 'The name of this option.',
            type: 'string',
        },
        {
            name: 'keywords',
            title: 'Keywords',
            description: 'The keywords associated with this option, used for autocompletion.',
            type: 'array',
            of: [{ type: 'string' }],
        },
    ],
}
    