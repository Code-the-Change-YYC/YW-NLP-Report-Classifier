import createSchema from 'part:@sanity/base/schema-creator'
import schemaTypes from 'all:part:@sanity/base/schema-type'

import cirForm from './cirForm'
import optionWithKeywords from './optionWithKeywords'

export default createSchema({
  name: 'default',
  types: schemaTypes.concat([
    cirForm,
    optionWithKeywords
  ])
})
