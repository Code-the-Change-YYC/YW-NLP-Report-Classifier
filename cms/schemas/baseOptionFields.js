export const NAME_FIELD = {
    name: 'name',
    title: 'Option Name',
    description: 'The name of this option.',
    type: 'string',
}

export const RISK_WEIGHTING_FIELD = {
    name: 'risk_weighting',
    title: 'Risk Weighting',
    description: 'The relative weight of choosing this option in the form. 1 = extremely low risk and 6 = extremely high risk.',
    type: 'string',
}

export const KEYWORDS_FIELD = {
    name: 'keywords',
    title: 'Keywords',
    description: 'The keywords associated with this option, used for autocompletion.',
    type: 'array',
    of: [{ type: 'string' }]
}