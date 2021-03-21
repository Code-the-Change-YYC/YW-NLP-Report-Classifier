import { NAME_FIELD, KEYWORDS_FIELD, RISK_WEIGHTING_FIELD } from './baseOptionFields';

export default {
    name: 'optionWithKeywordsAndRisk',
    type: 'object',
    fields: [
        NAME_FIELD,
        RISK_WEIGHTING_FIELD,
        KEYWORDS_FIELD
    ]
}
