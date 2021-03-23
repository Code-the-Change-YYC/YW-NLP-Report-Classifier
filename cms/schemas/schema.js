import createSchema from 'part:@sanity/base/schema-creator'
import schemaTypes from 'all:part:@sanity/base/schema-type'

import cirForm from './cirForm'
import option from './option'
import optionWithKeywords from './optionWithKeywords'
import optionWithRisk from './optionWithRisk'
import optionWithKeywordsAndRisk from './optionWithKeywordsAndRisk'

export default createSchema({
  name: 'default',
  types: schemaTypes.concat([
    cirForm,
    option,
    optionWithRisk,
    optionWithKeywords,
    optionWithKeywordsAndRisk
  ])
})
