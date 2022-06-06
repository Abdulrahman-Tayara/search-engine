import axiosBase from "../remote/axios";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom";
import "../App.scss";

import LoadingState from "../components/LoadingState";

function DocumentPage() {
    let { documentId } = useParams();

    const [document, setDocument] = useState(null);
    const [documentContent, setDocumentContent] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const history = useHistory();

    useEffect(() => {
        if (documentId) {
            axiosBase
                .get(`/documents/${documentId}`)
                .then((response) => {
                    const document = response.data.data;
                    setDocument(document)
                    setIsLoading(false);
                })
                .catch(function (error) {
                    console.error(error);
                });


        } else {
            // setTimeout(() => history.push(`/?search=${encodeURI(term)}`));
        }
    }, [documentId]);

    useEffect(() => {
        if (!document)
            return;

        axiosBase
            .get(`/documents/${documentId}/content`)
            .then((response) => {
                var documentContent = response.data.data;
                documentContent =
                    documentContent.replace(document.title, '').replace(document.authors.join("\n"), '')
                        .replace('\r\n', '')

                setDocumentContent(documentContent)
                setIsLoading(false);
            })
            .catch(function (error) {
                console.error(error);
            });
    }, [document])

    return (
        <section>
            {isLoading && <LoadingState />}
            {document && documentContent &&
                <div className="ika-center">
                    <h3>{document.title}</h3>

                    <div style={{ marginTop: '10px' }}>
                        {document.authors.map(author => {
                            return <h4>{author}</h4>
                        })}
                    </div>

                    <p style={{ marginTop: '30px' }}>{documentContent}</p>
                </div>
            }
        </section>
    );
}

export default DocumentPage;
