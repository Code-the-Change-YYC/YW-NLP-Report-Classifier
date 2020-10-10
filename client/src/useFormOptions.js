// language=GraphQL
const formQuery = `
    {
        CirForm(id: "cirForm") {
            primaryIncTypes
        }
    }
`

export async function useFormOptions() {
    try {
        const res = await fetch(process.env.REACT_APP_SANITY_GRAPHQL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
                Authorization: `Bearer ${process.env.REACT_APP_SANITY_READ_TOKEN}`,
            },
            body: JSON.stringify({ query: formQuery }),
        })
        const data = await res.json()
        console.log(data)
    } catch (e) {
        console.log(e)
    }
    return 0
}
