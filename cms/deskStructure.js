import S from '@sanity/desk-tool/structure-builder'

export default () =>
    S.list()
        .title('Content')
        .items([
            S.listItem()
                .title('Critical Incident Report Form')
                .child(S.editor().schemaType('cirForm').documentId('cirForm')),
            ...S.documentTypeListItems().filter(
                (listItem) => !['cirForm'].includes(listItem.getId())
            ),
        ])
