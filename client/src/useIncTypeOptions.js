import { useEffect, useState } from 'react'
import { getMultiPrediction } from './actions/predict'

function gql(str) {
    /**
     * Really high tech graphql parser so that VSCode and Prettier stop ignoring
     * my graphql strings.
     */
    return str[0]
}

const formQuery = gql`
    {
        CirForm(id: "cirForm") {
            primaryIncTypes
        }
    }
`

function incTypesToReactSelectOptions(incTypes) {
    return Object.assign(
        {},
        ...incTypes.map((incType) => {
            const value = incType.toLowerCase()
            return {
                [value]: {
                    value,
                    label: incType,
                },
            }
        })
    )
}

export function useIncTypeOptions() {
    const [incTypesOptions, setIncTypesOptions] = useState()
    const [incidentTypePri, setIncidentTypePri] = useState(null)

    async function fetchFormOptions() {
        const res = await fetch(process.env.REACT_APP_SANITY_GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
                Authorization: `Bearer ${process.env.REACT_APP_SANITY_READ_TOKEN}`,
            },
            body: JSON.stringify({ query: formQuery }),
        })
        const { data } = await res.json()
        const incTypes = data?.CirForm?.primaryIncTypes
        if (!incTypes) {
            return
        }
        setIncTypesOptions(incTypesToReactSelectOptions(incTypes))
    }

    async function updateOptionsFromDescription(description) {
        if (incTypesOptions) {
            const predictions = await getMultiPrediction(
                description,
                incTypesOptions
            )
            setIncTypesOptions(predictions)
            setIncidentTypePri(predictions[0])
        }
    }

    // Fetch options only on component load
    useEffect(() => {
        try {
            fetchFormOptions()
        } catch (e) {
            console.log('Error fetching from Sanity:', e)
        }
    }, [])

    const reactSelectOptions = incTypesOptions
        ? Object.values(incTypesOptions)
        : null

    return {
        incidentTypePri,
        setIncidentTypePri,
        reactSelectOptions,
        updateOptionsFromDescription,
    }
}
