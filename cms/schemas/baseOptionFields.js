export const NAME_FIELD = {
    name: 'name',
    title: 'Option Name',
    description: 'The name of this option.',
    type: 'string',
    validation: Rule => Rule.required().min(1).max(200)
}

export const RISK_WEIGHTING_FIELD = {
    name: 'risk_weighting',
    title: 'Risk Weighting',
    description:
        'The relative weight of choosing this option in the form. 1 = extremely low risk and 6 = extremely high risk.',
    type: 'number',
    validation: (Rule) =>
        Rule.required()
            .integer()
            .min(1)
            .max(6)
            .error('Must be an integer between 1 and 6.'),
}

export const KEYWORDS_FIELD = {
    name: 'keywords',
    title: 'Keywords',
    description:
        'The keywords associated with this option, used for autocompletion.',
    type: 'array',
    of: [{ type: 'string' }],
    validation: (Rule) =>
        Rule.custom((keywords) => {
            const kwMaxLength = 200
            const kwMinLength = 1
            // Keywords are valid if: 1. there are none (undefined), or 2. They
            // meet the length requirements. Otherwise there is an error
            return (
                typeof keywords === 'undefined' ||
                keywords.every(
                    (kw) => kw.length <= kwMaxLength && kw.length >= kwMinLength
                ) ||
                'Keywords must be under 50 characters'
            )
        }),
}