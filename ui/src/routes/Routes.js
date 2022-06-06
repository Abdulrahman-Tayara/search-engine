import { Switch, Route, BrowserRouter as Router } from "react-router-dom";
import DocumentPage from "../pages/DocumentPage";

// Pages
import Home from "../pages/HomePage";
import Search from "../pages/SearchPage";

function Routes() {
  return (
    <Router>
      <Switch>
        <Route exact path="/(|search)" component>
          <Home />
        </Route>
        <Route exact path="/search/:term" component>
          <Search />
        </Route>
        <Route exact path="/document/:documentId" component>
          <DocumentPage />
        </Route>
      </Switch>
    </Router>
  );
}

export default Routes;
