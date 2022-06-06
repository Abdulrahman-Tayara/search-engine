import React, { useState } from 'react'
import { useHistory } from "react-router-dom";


function SearchBarTop({ term }) {
    const [searchFor, setSearchFor] = useState("");
    const history = useHistory();

    const triggerSearch = (e) => {
        e.preventDefault();

        if (searchFor) {

            setTimeout(() => history.push(`/search/${encodeURI(searchFor)}`));
        }
    };


    return (
        <nav className="nav-yapa-mwamba">
            
            <form onSubmit={triggerSearch} style={{ marginTop: "20px" }}>
                <div className="foresight-search-bar fill-space m-bottom">
                    <input
                        value={searchFor}
                        onChange={(e) => {
                            setSearchFor(e.target.value);
                        }}
                        type="text"
                        placeholder={term}
                    />
                    <i className="material-icons">search</i>
                </div>
            </form>
        </nav>
    )
}

export default SearchBarTop
