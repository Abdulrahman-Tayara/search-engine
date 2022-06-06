import axiosBase from "../remote/axios";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom";
import "../App.scss";

import LoadingState from "../components/LoadingState";
import SearchBarTop from "../components/SearchBarTop";
import NoDataState from "../components/NoDataState";

function Search() {
  let { term } = useParams();

  const [returnedSearch, setReturnedSearch] = useState([]);
  const [correct, setCorrect] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEmpty, setEmpty] = useState(false);

  const history = useHistory();
  useEffect(() => {
    if (term) {
      correctQuery()
      setIsLoading(true);
      axiosBase
        .post('/search', { query: term })
        .then((response) => {
          const data = response.data.data;
          setReturnedSearch(data);
          setIsLoading(false);
          setEmpty(data.length === 0)
        })
        .catch(function (error) {
          console.error(error);
        });
    } else {
      setTimeout(() => history.push(`/?search=${encodeURI(term)}`));
    }
  }, [term]);

  const correctQuery = () => {
    axiosBase
      .post('/correct', { query: term })
      .then((response) => {
        const correctedQuery = response.data.data;

        if (correctedQuery !== term) {
          setCorrect(correctedQuery);
        } else {
          setCorrect(null);
        }
      })
      .catch(function (error) {
        console.error(error);
      });
  }

  const onDocumentClick = (document) => {
    history.push(`/document/${document._id}`)
  }

  const updateWithCorrectedQuery = () => {
    history.replace(`/search/${encodeURI(correct)}`)
  }

  return (
    <section>

      <SearchBarTop term={term} />

      {correct &&
        <div className="ika-center">
          <p>Do you mean: </p>
          <p onClick={updateWithCorrectedQuery}><u>{correct}</u></p>
        </div>
      }

      <div className="ika-center">
        <ul>
          {isLoading && <LoadingState />}
          {isEmpty && <NoDataState />}
          {returnedSearch.map((result, index) => (
            <li className="ka-box-one-search" key={index} onClick={() => onDocumentClick(result)}>
              <h3>{result.title}</h3>
              {result.authors.map(author => {
                return <pre>{author}</pre>
              })}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default Search;
