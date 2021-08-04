// ALL REQUESTS PAGE
class All_Requests extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        var url = '/api/get_requests' + window.location.search

        return(
            <Request_Parent url={url} username={this.props.username}/>
        );
    }

}

class Request_Parent extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: true,
            requests_ids: [],
            err: null,
            first_page: 1,
            last_page: 1,
            actual_page: null,
            has_next: false,
            has_previous: false,
        }
    }

    updateState(jsondata){
        this.setState({
            requests_ids: jsondata['ids'], 
            first_page: jsondata['first_page'], 
            last_page: jsondata['last_page'], 
            actual_page: jsondata['actual_page'], 
            has_next: jsondata['has_next'], 
            has_previous: jsondata['has_previous'], 
            is_loading: false,
        })
    }

    componentDidMount() {
        
        // define requests ids and pagination
        fetch(this.props.url)
            .then(response => { 
                if (response.status===200) {
                    return response.json();
                } else if (response.status===204) {
                    throw new Error('You have no requests..');
                } else {
                    throw new Error('API Error: get_requests');
                }
            })
            .then(jsondata => {
                if (jsondata['ids'][0] === null) {
                    throw new Error('No requests');
                } else {
                    this.updateState(jsondata);
                }
            })
            .catch(error => this.setState({err: error.message, is_loading: false}));

    }
        
    render() {

        const requests_ids = this.state.requests_ids;

        if (this.state.err) {
            //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else {
            return (
                <div className="container text-center">
                    <Paginator has_next={this.state.has_next} has_previous={this.state.has_previous} first_page={this.state.first_page} last_page={this.state.last_page} actual_page={this.state.actual_page}/>
                    
                    <div className="row">
                        <div className="col">
                            {requests_ids.map(id => (<Request key={id} request_id={id} username={this.props.username}/>))}
                        </div>
                    </div>
                </div>
            );
        }
    }
}

class Request extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            requester_username: null,
            is_loading: true,
            request_title: "",
            request_category: "",
            request_definition: "",
            request_goal: "",
            request_context: "",
            request_restrictions: "",
            request_offer_value: "",
            request_ideas_count: 0,
            err: null,
        }
    }

    show_details(){
        let id = "details_"+this.props.request_id;
        var btn_id = "btn_details_"+this.props.request_id;
        var hid = document.getElementById(id).hidden;
        
        if (hid) {
            document.getElementById(id).hidden = false;
            document.getElementById(btn_id).innerHTML = "Hide Details";
        } else {
            document.getElementById(id).hidden = true;
            document.getElementById(btn_id).innerHTML = "Show Details";
            
        }
    }

    componentDidMount() {
        
        var url
        url = "/api/get_request/"+this.props.request_id

        fetch(url)
            .then(response => { 
                if (response.status===200) {
                    return response.json();
                } else if (response.status===204) {
                    throw new Error('No content found');
                } else {
                    throw new Error('API Error: get_request');
                }
        })
        .then(jsondata => {
            this.setState({
                requester_username: jsondata['requester_username'],
                request_title: jsondata['title'],
                request_category: jsondata['request_category'],
                request_definition: jsondata['request_definition'],
                request_goal: jsondata['goal'],
                request_context: jsondata['context'],
                request_restrictions: jsondata['restrictions'],
                request_offer_value: jsondata['offer_value'],
                offered_ideas_count: jsondata['offered_ideas_count'],
                is_loading: false,
            })
        })
        .catch(error => this.setState({err: error.message, is_loading: false}));
    }

    btnRequest(){
        if (this.state.requester_username == this.props.username) {
            return "CHECK IDEAS";
        } else {
            return "OFFER NEW IDEA";
        }
    }

    render() {
        if (this.state.err) {
        //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else if (this.state.is_loading) {
            return (
                <div className="container text-left my-3 request-element">
                    <div className="row my-3">
                        <div className="col">
                            <div className="loader"></div>
                        </div>
                    </div>
                </div>
                );   
            
        } else {
            return (
            <div className="container text-left my-3 request-element">
                <div className="row">
                    <div className="col">
                        <a className="text-info" href={"/request/"+this.props.request_id}><h3>{this.state.request_title}</h3></a>
                        <a className="text-info" href={"/request/"+this.props.request_id}><img src="/media/idea_icon.png" height="25px" width="25px"></img> Ideas: {this.state.offered_ideas_count}</a><br/>  
                    </div>
                    <div className="col text-right">
                        <p>Category: {this.state.request_category}</p>
                        <p>{this.state.request_definition}</p>

                    </div>
                </div>
                <div className="row mt-2 justify-content-between">
                    <div className="col">
                        <h6>Goal: {this.state.request_goal}</h6>
                    </div>
                    <div className="col text-right">
                        <span className="price alert alert-danger"> USD {this.state.request_offer_value}</span>
                    </div>
                </div>
                <div className="row mt-2 justify-content-between">
                    <div className="col">
                        <button id={"btn_details_"+this.props.request_id} className="btn btn-outline-secondary mb-2 mr-2 horiz_expand" onClick={() => this.show_details()}>Show Details</button>
                        <a id={"btn_request_"+this.props.request_id} href={"/request/"+this.props.request_id}><button className="btn_new_idea btn btn-info mb-2 horiz_expand">{this.btnRequest()}</button></a>
                        
                    </div>
                    <div className="col username">
                        <span className="div-bottom"><small>requested by @{this.state.requester_username}</small></span>
                    </div>
                </div>
                <div className="row ">
                    <div className="col">
                        <div id={"details_"+this.props.request_id} hidden>
                            <p>Context:</p>
                            <textarea rows="4" className="request-text form-control my-2" type="text" value={this.state.request_context} readOnly></textarea>
                            <p>Restrictions:</p>
                            <textarea rows="4" className="request-text form-control my-2" type="text" value={this.state.request_restrictions} readOnly></textarea>
                        </div>
                    </div>
                </div>
                
            </div>
            );
        }
    }
}


// MY REQUESTS PAGE

class My_Requests extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        var url = '/api/get_my_requests_ids'+ window.location.search

        return(
            <Request_Parent url={url} username={this.props.username}/>
        );
    }

}


// MY IDEAS PAGE


class My_Ideas extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        var url = '/api/get_my_ideas_ids'+ window.location.search

        return(
            <Ideas_Parent url={url}/>
        );
    }

}

class Ideas_Parent extends React.Component {    

    constructor(props){
        super(props);
        this.state = {
            is_loading: true,
            shared_ideas_ids: [],
            err: null,
            first_page: 1,
            last_page: 1,
            actual_page: null,
            has_next: false,
            has_previous: false,
        }
    }

    updateState(jsondata){
        this.setState({
            shared_ideas_ids: jsondata['ids'], 
            first_page: jsondata['first_page'], 
            last_page: jsondata['last_page'], 
            actual_page: jsondata['actual_page'], 
            has_next: jsondata['has_next'], 
            has_previous: jsondata['has_previous'], 
            is_loading: false
        })
    }

    componentDidMount() {    

        fetch(this.props.url)
            .then(response => { 
                if (response.status===200) {
                    return response.json()
                } else if (response.status===204) {
                    throw new Error('You have no ideas.');
                } else {
                    throw new Error('API Error: get_ideas_ids');
                }
            })
            .then(response => this.updateState(response))
            .catch(error => this.setState({err: error.message, is_loading: false}));
    }

    render() {

        if (this.state.err) {
            //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );                
        } else {
            const shared_ideas_ids = this.state.shared_ideas_ids;

            return (
                <div className="container text-center">
                    <Paginator has_next={this.state.has_next} has_previous={this.state.has_previous} first_page={this.state.first_page} last_page={this.state.last_page} actual_page={this.state.actual_page}/>

                    <div className="row">
                        <div className="col">
                            {shared_ideas_ids.map(id => (<Idea key={id} idea_id={id}/>))}
                        </div>
                    </div>
                </div>
            );
        }
    }
}

class Idea extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: true,
            idea_request_title: null,
            idea_title: null,
            idealist: null,
            idea_request_id: null,
            idea_request_category: null,
            idea_request_definition: null,
            idea_content: "",
            share_value: null,
            idea_attachments: null,
            err: null,
            status: null,
        }
    }

    componentDidMount() {
        
        var url
        url = "/api/get_idea/" + this.props.idea_id

        fetch(url)
            .then(response => { 
                if (response.status===200) {
                    return response.json();
                } else if (response.status===204) {
                    throw new Error('No content found');
                } else {
                    throw new Error('API Error: get_idea');
                }
            })
            .then(jsondata => {
                this.setState({
                    idea_request_title: jsondata['idea_request_title'],
                    idea_title: jsondata['idea_title'],
                    idealist: jsondata['idealist_username'],
                    idea_request_id: jsondata['idea_request_id'],
                    idea_request_category: jsondata['idea_request_category'],
                    idea_request_definition: jsondata['idea_request_definition'],
                    idea_content: jsondata['content'],
                    idea_attachments: jsondata['attachments'],
                    share_value: jsondata['share_value'],
                    status: jsondata['status'],
                    is_loading: false,
                })
            })
            .catch(error => this.setState({err: error.message, is_loading: false}));
            

    }

    show_details(){
        let id = "details_"+this.props.idea_id;
        var btn_id = "btn_details_"+this.props.idea_id;
        var hid = document.getElementById(id).hidden;
        
        if (hid) {
            document.getElementById(id).hidden = false;
            document.getElementById(btn_id).innerHTML = "Hide Details";
        } else {
            document.getElementById(id).hidden = true;
            document.getElementById(btn_id).innerHTML = "Show Details";
            
        }
    }

    priceColor(){
        if (this.state.status == "offered")
            return "price alert alert-warning";
        else if (this.state.status == "shared"){
            return "price alert alert-success";
        } 
    }


    render() {


        if (this.state.err) {
        //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else if (this.state.is_loading) {
            return (
                <div className="container text-left my-3 request-element text-secondary">
                    <div className="row my-3">
                        <div className="col">
                            <div className="loader"></div>
                        </div>
                    </div>
                </div>
                );   
            
        } else {
            return (
                <div className="container text-left my-3 request-element text-secondary">
                <div className="row">
                    <div className="col">
                        <h3>{this.state.idea_title}</h3>
                        In reply of: <a className="text-info" href={"/request/"+this.state.idea_request_id}>{this.state.idea_request_title}</a>
                    </div>
                    <div className="col text-right">
                        <p>Category: {this.state.idea_request_category}</p>
                        <p>{this.state.idea_request_definition}</p>

                    </div>
                </div>
                <div className="row mt-2 justify-content-between">
                    <div className="col">
                        <h6>Idea Value: USD {this.state.share_value} </h6>
                    </div>
                    <div className="col text-right">
                        <span className={this.priceColor()}> {this.state.status }</span>
                    </div>
                </div>
                <div className="row mt-2 justify-between">
                    <div className="col">
                        <button id={"btn_details_"+this.props.idea_id} className="btn btn-outline-secondary mb-2 mr-2" onClick={() => this.show_details()}>Show Details</button>
                        
                    </div>
                    <div className="col username">
                        <span className="div-bottom"><small>shared by @{this.state.idealist}</small></span>
                    </div>
                </div>
                <div className="row ">
                    <div className="col">
                        <div id={"details_"+this.props.idea_id} hidden>
                            <p>Content:</p>
                            <textarea rows="4" className="request-text form-control my-2" type="text" value={this.state.idea_content} readOnly></textarea>
                        </div>
                    </div>
                </div>

                </div>
            );
        }
    }
}

// IDEA PAGE
class Single_Idea extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        return(
            <IdeaPage key={this.props.id} idea_id={this.props.idea_id}/>
        );
    }

}

class IdeaPage extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: true,
            idea_request_title: null,
            idea_title: null,
            idealist: null,
            idea_request_id: null,
            idea_request_category: null,
            idea_request_definition: null,
            idea_content: "",
            share_value: null,
            idea_attachments: null,
            err: null,
            status: null,
        }
    }

    componentDidMount() {
        
        var url
        url = "/api/get_idea/" + this.props.idea_id

        fetch(url)
            .then(response => { 
                if (response.status===200) {
                    return response.json();
                } else if (response.status===204) {
                    throw new Error('No content found');
                } else {
                    throw new Error('API Error: get_idea');
                }
            })
            .then(jsondata => {
                this.setState({
                    idea_request_title: jsondata['idea_request_title'],
                    idea_title: jsondata['idea_title'],
                    idealist: jsondata['idealist_username'],
                    idea_request_id: jsondata['idea_request_id'],
                    idea_request_category: jsondata['idea_request_category'],
                    idea_request_definition: jsondata['idea_request_definition'],
                    idea_content: jsondata['content'],
                    idea_attachments: jsondata['attachments'],
                    share_value: jsondata['share_value'],
                    status: jsondata['status'],
                    is_loading: false,
                })
            })
            .catch(error => this.setState({err: error.message, is_loading: false}));
            

    }

    show_details(){
        let id = "details_"+this.props.request_id;
        var btn_id = "btn_details_"+this.props.request_id;
        var hid = document.getElementById(id).hidden;
        
        if (hid) {
            document.getElementById(id).hidden = false;
            document.getElementById(btn_id).innerHTML = "Hide Details";
        } else {
            document.getElementById(id).hidden = true;
            document.getElementById(btn_id).innerHTML = "Show Details";
            
        }
    }

    priceColor(){
        if (this.state.status == "offered")
            return "price alert alert-warning";
        else if (this.state.status == "shared"){
            return "price alert alert-success";
        } 
    }


    render() {


        if (this.state.err) {
        //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else if (this.state.is_loading) {
            return (
                <div className="container text-left my-3 request-element">
                    <div className="row my-3">
                        <div className="col">
                            <div className="loader"></div>
                        </div>
                    </div>
                </div>
                );   
            
        } else {
            return (
                <div className="container text-left my-3 request-element text-secondary">
                <div className="row">
                    <div className="col">
                        <h3>{this.state.idea_title}</h3>
                        In reply of: <a className="text-info" href={"/request/"+this.state.idea_request_id}>{this.state.idea_request_title}</a>
                    </div>
                    <div className="col text-right">
                        <p>Category: {this.state.idea_request_category}</p>
                        <p>{this.state.idea_request_definition}</p>

                    </div>
                </div>
                <div className="row mt-2 justify-content-between">
                    <div className="col">
                        <h6>Idea Value: USD {this.state.share_value} </h6>
                    </div>
                    <div className="col-2 text-right">
                        <span className={this.priceColor()}> {this.state.status }</span>
                    </div>
                </div>
                <div className="row mt-2 justify-between">
                    <div className="col">
                        <button id={"btn_details_"+this.props.request_id} className="btn btn-outline-secondary mb-2 mr-2" onClick={() => this.show_details()}>Show Details</button>
                        
                    </div>
                    <div className="col username">
                        <span className="div-bottom"><small>shared by @{this.state.idealist}</small></span>
                    </div>
                </div>
                <div className="row ">
                    <div className="col">
                        <div id={"details_"+this.props.request_id} hidden>
                            <p>Content:</p>
                            <textarea rows="4" className="request-text form-control my-2" type="text" value={this.state.idea_content} readOnly></textarea>
                        </div>
                    </div>
                </div>

                </div>
            );
        }
    }
}


// IDEAS SHARED PAGE

class Shared_Ideas extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        var url = '/api/get_my_shared_ideas_ids'+ window.location.search

        return(
            <Ideas_Parent url={url}/>
        );
    }

}


// SINGLE REQUEST PAGE

class Single_Request_Parent extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: false,
            requests_ids: [this.props.request_id],
            err: null,
        }
    }
        
    render() {
        const requests_ids = this.state.requests_ids;


        if (this.state.err) {
            //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else if (this.state.is_loading) {
            return (
                <div className="container text-left my-3 request-element">
                    <div className="row my-3">
                        <div className="col">
                            <div className="loader"></div>
                        </div>
                    </div>
                </div>
            );   
                
        } else {
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {requests_ids.map(id => (<Single_Request key={id} request_id={id} request_username={this.props.request_username} />))}
                        </div>

                    </div>
                </div>
            );
        }
    }
}

class Single_Request extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            requester_username: null,
            is_loading: true,
            request_title: null,
            request_subject: null,
            request_goal: "",
            request_context: "",
            request_restrictions: "",
            request_offer_value: null,
            err: null,
        }
    }

    displayHideIdeas(e) {

        if (e.target.id == "showideas") {
            document.querySelector("#ideas_preview").style.display = "block";
            document.querySelector("#showideas").innerText = "HIDE IDEAS";
            document.querySelector("#showideas").id = "hideideas";
        } else if ((e.target.id == "hideideas")){
            document.querySelector("#ideas_preview").style.display = "none";
            document.querySelector("#hideideas").innerText = "CHECK OUT IDEAS";
            document.querySelector("#hideideas").id = "showideas";
        }
    }

    componentDidMount() {
        
        var url = "/api/get_request/"+this.props.request_id

        fetch(url)
        .then(response => { 
            if (response.status===200) {
                return response.json();
            } else if (response.status===204) {
                throw new Error('No content found');
            } else {
                throw new Error('API Error: get_request');
            }
        })
        .then(jsondata => {
            this.setState({
                requester_username: jsondata['requester_username'],
                request_title: jsondata['title'],
                request_category: jsondata['request_category'],
                request_definition: jsondata['request_definition'],
                request_goal: jsondata['goal'],
                request_context: jsondata['context'],
                request_restrictions: jsondata['restrictions'],
                request_offer_value: jsondata['offer_value'],
                offered_ideas_count: jsondata['offered_ideas_count'],
                shared_ideas_count: jsondata['shared_ideas_count'],
                is_loading: false,
            })
        })
        .catch(error => this.setState({err: error.message, is_loading: false}));

        document.getElementById("new_idea_create").onclick = () => {
            document.querySelectorAll(".new_idea").forEach( element => {
                element.style.display = "block";
            });
        };
    }

    show_details(){
        let id = "details_"+this.props.request_id;
        var btn_id = "btn_details_"+this.props.request_id;
        var hid = document.getElementById(id).hidden;
        
        if (hid) {
            document.getElementById(id).hidden = false;
            document.getElementById(btn_id).innerHTML = "Hide Details";
        } else {
            document.getElementById(id).hidden = true;
            document.getElementById(btn_id).innerHTML = "Show Details";
            
        }
    }

    render() {

        if (this.state.err) {
        //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else {
            return (
            <div className="container text-left my-3">
                <div className="d-flex flex-row justify-content-between">
                    <div className="d-flex col-8 px-0">
                        <a className="text-info" href={"/request/"+this.props.request_id}><h1>{this.state.request_title}</h1></a>
                    </div>
                    <div className="d-flex mt-3 vert_expand">
                        <span className="price alert alert-danger">$ {this.state.request_offer_value}</span>
                    </div>
                </div>
                <div className="row align-items-center ">
                    <div className="col-auto mr-auto">
                        <button className="btn btn-info mr-2" id={"btn_details_"+this.props.request_id} onClick={() => this.show_details()}>Show Details</button>

                        { this.props.request_username==this.state.requester_username
                        ? <button id="hideideas" className="btn btn-outline-info" onClick={ (e) => this.displayHideIdeas(e)}>HIDE IDEAS</button>
                        : <button id="new_idea_create" className="btn btn-dark my-1">CREATE IDEA</button>
                        }
                    </div>
                    <div className="col-auto ml-auto text-right">
                        <p>Category: {this.state.request_category}</p>
                        <p>{this.state.request_definition}</p>

                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-auto">
                        <button className="btn btn-outline-success"><span className="ideas-count">{this.state.shared_ideas_count}</span><br/><span>Ideas Shared</span></button>                        
                    </div>
                    <div className="col-auto">
                        <button className="btn btn-outline-warning"><span className="ideas-count">{this.state.offered_ideas_count}</span><br/><span>Ideas Offered</span></button>
                    </div>
                    <div className="col-auto ml-auto username">
                        <span className="div-bottom"><small>requested by @{this.state.requester_username}</small></span>
                    </div>
                </div>

                <div className="row ">
                    <div className="col">
                        <div id={"details_"+this.props.request_id} hidden>
                            <p>Goal: </p>
                            <textarea rows="1" className="request-text form-control my-2" type="text" value={this.state.request_goal} readOnly></textarea>
                            <p>Context:</p>
                            <textarea rows="4" className="request-text form-control my-2" type="text" value={this.state.request_context} readOnly></textarea>
                            <p>Restrictions:</p>
                            <textarea rows="4" className="request-text form-control my-2" type="text" value={this.state.request_restrictions} readOnly></textarea>
                        </div>
                    </div>
                </div>
                <New_Idea request_id={this.props.request_id} offer_value={this.state.request_offer_value}/>
            </div>
            );
        }
    }
}

class Preview_Shared_Ideas extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        var url = '/api/get_ideas_from_requests_ids/' + this.props.request_id

        return(
            <div>
                <div className="row">
                    <div id="accept_pay_error" className="col alert alert-danger text-center" role="alert" hidden>
                    </div>                        
                </div>

                <Preview_Ideas_Parent url={url} request_username={this.props.request_username}/>
            </div>
        );
    }

}

class Preview_Ideas_Parent extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: true,
            shared_ideas_ids: [],
            err: null,
        }
    }


    componentDidMount() {    

        fetch(this.props.url)
            .then(response => { 
                if (response.status===200) {
                    return response.json();
                } else if (response.status===204) {
                    throw new Error('User has no shared_ideas');
                } else {
                    throw new Error('API Error: get_shared_ideas_ids');
                }
            })
            .then(jsondata => {

                if (jsondata['ids'] === null) {
                    throw new Error('User has no ideas shared');
                } else {
                    this.setState({shared_ideas_ids: jsondata['ids'], is_loading: false})
                }
            })
            .catch(error => this.setState({err: error.message, is_loading: false}));

    }
        
    render() {

        const shared_ideas_ids = this.state.shared_ideas_ids;


        if (this.state.err) {
            //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else if (this.state.is_loading) {
            return (
                <div className="container text-left my-3 request-element">
                    <div className="row my-3">
                        <div className="col">
                            <div className="loader"></div>
                        </div>
                    </div>
                </div>
            );   
                
        } else {
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {shared_ideas_ids.map(id => (<Preview_Idea key={id} idea_id={id} request_username={this.props.request_username }/>))}
                        </div>
                    </div>
                </div>
            );
        }
    }
}

class Preview_Idea extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: true,
            idealist: null,
            idea_request_id: null,
            idea_timestamp: null,
            idea_status: null,
            rating: null,
            share_value: null,
            err: null,
        }
        this.shareIdeaState=this.shareIdeaState.bind(this);
    }

    componentDidMount() {
        
        var url = "/api/get_idea_preview/" + this.props.idea_id

        fetch(url)
            .then(response => { 
                if (response.status===200) {
                    return response.json();
                } else if (response.status===204) {
                    throw new Error('No content found');
                } else {
                    throw new Error('API Error: get_idea_preview');
                }
            })
            .then(jsondata => {
                this.setState({
                    idealist: jsondata['idealist__username'],
                    share_value: jsondata['share_value'],
                    rating: jsondata['rating'],
                    idea_timestamp: jsondata['timestamp'],
                    idea_status: jsondata['status'],
                    is_loading: false,
                })
            })
            .catch(error => this.setState({err: error.message, is_loading: false}));

    }

    shareIdeaState() {
        this.setState({ "idea_status": "shared"})
    }

    display_payment_box() {
        //Stripe variable for stripe
        var stripe = Stripe('pk_test_51I1kZwF2Gy9eFZtoKSGPFTaP5BqN2Kg6Lt0UhJfAsCxa3aW0uwWuKvQuzYdFAiNks7UyVgcDVgOt83uWZosCx95o00H2ohFmeq');

        var id="#payment_box_idea_"+this.props.idea_id
        document.querySelectorAll(".payment_box_idea").forEach( element => {
            element.style.display = "none";
        });
        document.querySelectorAll(".credit_cards_box").forEach( element => {
            element.style.display = "none";
        });
        document.querySelector(id).style.display = "block"
        var id = "#credit_cards_box_"+this.props.idea_id
        document.querySelector(id).style.display = "block";
    
    
        //mount element
        
        var elements = stripe.elements();
        var style = {

            base: {
              color: "#6C757D",
              fontWeight: 500,
              fontFamily: "Inter UI, Open Sans, Segoe UI, sans-serif",
              fontSize: "16px",
              fontSmoothing: "antialiased",
      
              "::placeholder": {
                color: "#17A2B8"
              }
            },
            invalid: {
              color: "#E25950"
            }
          }
        
        var card = elements.create("card", {style: style });
        var card_element="#card_element_"+this.props.idea_id
        card.mount(card_element);
    
        var card_errors_id = "card_errors_"+this.props.idea_id
    
        card.on('change', function(event) {
            var displayError = document.getElementById(card_errors_id);
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
            });

        var form_id = "payment_form_"+this.props.idea_id
        var paymentForm = document.getElementById(form_id)
        paymentForm.addEventListener("submit", (event) => this.paymentForm(event, card, stripe));
    }

    async paymentForm(event, card, stripe) {

        event.preventDefault();
        var clientSecret = await this.create_payment_intent();
        // console.log(clientSecret);
        const payment = await this.execute_payment(clientSecret, card, stripe);

        if (payment) {
            this.shareIdeaState();
        };
    }
       
    async create_payment_intent() {

        var url = "/stripe_create_intent/"+this.props.idea_id
        
        const responsejson = await fetch(url)
        .then(response => {
            return response.json()
        })
        .then( jsondata => {
            if (jsondata.error_accept){
                document.getElementById("accept_pay_error").innerHTML = "To buy an idea you must <a href='/paymentinfo'>accept</a> the Terms of Usage.";
                document.getElementById("accept_pay_error").hidden = false;
                console.log("err_accept")
            } else {
                return jsondata;
            }
        });

   
        var client_secret = await responsejson.client_secret
    
        return await client_secret;
    }

    async execute_payment(clientSecret, card, stripe) {
    
        const confirmation = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
            }
        })
        .then(function(result) {
            if (result.error) {
            // Show error to your customer (e.g., insufficient funds)
                alert(result.error.message);
                return false;
            } else {
            // The payment has been processed!
                if (result.paymentIntent.status === 'succeeded') {
                    alert("Payment cofirmed. You can review your idea.");
                    return true;

                    // post-payment actions are handled by webhook
                }
            }
        });
    
        return confirmation;
    } 

    render() {
        if (this.state.err) {
        //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else if (this.state.is_loading) {
            return (
                <div className="container text-left my-3 request-element">
                    <div className="row my-3">
                        <div className="col">
                            <div className="loader"></div>
                        </div>
                    </div>
                </div>                
                );
        } else {
            return (
                <div className="container text-center my-3 request-element">
                    <div className="row">
                        <div className="col-6 col-lg-3 my-2 align-self-center">
                            <h5>Idea from: @{this.state.idealist}</h5>
                            <h6>Eureka date was {this.state.idea_timestamp}</h6>
                        </div>
                        <div className="col-6 col-lg-2 align-self-center">
                            {this.state.idea_status == "shared"
                                ? <a href={"/idea/"+this.props.idea_id}><button id="review_idea" className="btn btn-info my-1">REVIEW IDEA</button></a>
                                : <button id="payment_intent" className="btn btn-outline-danger my-1"onClick={ (ev) => {
                                    this.display_payment_box();
                                }}>BUY IDEA</button>
                            }

                        </div>
                        <div className="col-12 col-lg-7 payment_box_idea align-self-center my-2" id={"payment_box_idea_"+this.props.idea_id}>
                            <div className="row">
                                <div className="col">
                                    <PayCardParent idea_id={this.props.idea_id} shareIdeaState={this.shareIdeaState}/>
                                </div>

                                <div className="col card_box_idea align-self-center">
                                    <input hidden id={"client_secret_"+this.props.idea_id}></input>
                                    <input hidden id={"payment_method_"+this.props.idea_id} name="payment_method"></input>

                                    <form id={"payment_form_"+this.props.idea_id} className="text-center">
                                        <div className="card_input" id={"card_element_"+this.props.idea_id}>
                                        </div>

                                        <div id={"card_errors_"+this.props.idea_id} role="alert"></div>

                                        <button className="btn btn-info mt-2 py-0" id={"submit_"+this.props.idea_id}>Pay</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    }
}

class PayCardParent extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            loading: false,
            cards: [],
        };
        this.getCustomerCards = this.getCustomerCards.bind(this);
        this.parentShareIdeaState = this.parentShareIdeaState.bind(this);
    }

    getCustomerCards() {
        fetch("/stripe/list_cards")
        .then(response => {
            return response.json();
        })
        .then(data => {
            this.setState({cards: data});
        })

    }

    componentDidMount() {
        this.getCustomerCards();
    }

    parentShareIdeaState(){
        this.props.shareIdeaState();
    }

    render() {
        const cards = this.state.cards;
        var list_cards = [];
        Object.values(cards).map( entry => {
            list_cards.push(Object.values(entry));
        })

        return(
            <div id={"credit_cards_box_"+this.props.idea_id} className="credit_cards_box">
                {list_cards.map( (card, index) => <Select_Credit_Card_Pay key={index} card_id={card[0]} brand={card[1]} last4={card[2]} idea_id={this.props.idea_id} shareIdeaState={this.parentShareIdeaState}/>)}
                <a href="/paymentinfo"><button className="btn btn-info mt-0 mb-2 py-0">Manage Cards</button></a>
            </div>
        );
    }
}

class Select_Credit_Card_Pay extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: false,
        }
        this.btnIdeaShareState = this.btnIdeaShareState.bind(this);
    }

    btnIdeaShareState(){
        this.props.shareIdeaState();
    }

    async payCardButton(){
        var stripe = Stripe('pk_test_51I1kZwF2Gy9eFZtoKSGPFTaP5BqN2Kg6Lt0UhJfAsCxa3aW0uwWuKvQuzYdFAiNks7UyVgcDVgOt83uWZosCx95o00H2ohFmeq');

        const clientSecret = await this.create_payment_intent();

        var confirmation = await stripe.confirmCardPayment(clientSecret, {
            payment_method: this.props.card_id
          }).then(function(result) {
            if (result.error) {
              // Show error to your customer
                console.log(result.error.message);
                return false;
            } else {
              if (result.paymentIntent.status === 'succeeded') {
                alert("Payment cofirmed. You can review your idea.");
                return true;
              }
            }
          });

        if (confirmation) {
            this.btnIdeaShareState();
        }
    }

    async create_payment_intent() {
        var url = "/stripe_create_intent/"+this.props.idea_id+"?"+"payment_method="+this.props.card_id
        
        const response = await fetch(url);
        const responsejson = await response.json();
        var client_secret = responsejson.client_secret
    
        return await client_secret;
    }

    render() {
        if (this.state.err) {
            //render element for loading error
                return (
                    <div className="container text-center">
                        <div className="row">
                            <div className="col">
                                {this.state.err}.
                            </div>
                        </div>
                    </div>
                );
            } else if (this.state.is_loading) {
                return (
                    <div className="container text-left my-3 request-element">
                        <div className="row my-3">
                            <div className="col">
                                <div className="loader"></div>
                            </div>
                        </div>
                    </div>
                    );   
            } else {
                return (
                    <div className="row my-2 justify-content-center">
                    	    <div className="card_number">**** **** **** {this.props.last4}</div>
                            <button className="btn btn-outline-info py-0" onClick={() => this.payCardButton()}>Pay with Card</button>
                    </div>
                );
            }
    }
}

class New_Idea extends React.Component {
    constructor(props){
        super(props);
        this.state = {}
    }

    newIdeaCancel() {
        document.querySelectorAll(".new_idea").forEach( element => {
            element.style.display = "none";
        });
    }


    async newIdeaSubmit(e) {
        e.preventDefault();

        document.getElementById("idea_request").value = this.props.request_id;
        const new_idea_form = document.getElementById("new_idea_form")

        let response = await fetch('/api/new_idea', {
            method: 'POST',
            body: new FormData(new_idea_form)
        });

        let result = await response.json();
        
        if (result.error) {
            document.getElementById("msg_errors_box").style.display = "block";
            document.getElementById("msg_errors").innerHTML = JSON.stringify(result.error);
        } else if (result.error_accept){
            document.getElementById("msg_errors_box").style.display = "block";
            document.getElementById("msg_errors").innerHTML = "<span>To share ideas, you must <a href='/paymentinfo'>accept</a> the Terms of Usage and set up your Banking Information</span>"    
        } else {
            window.location.href ="/my_ideas";
        }
    };


    render() {
        return(
            <div className="new_idea text-left my-2">

                <div id="msg_errors_box" className="alert alert-danger" role="alert">
                    <ul id="msg_errors"></ul>
                </div>

                <form id="new_idea_form" onSubmit={ (e) => this.newIdeaSubmit(e, this.props.request_id, this.props.offer_value)}>
                    <CSRFToken/>
                    <input type="hidden" id="idea_request" name="idea_request" readOnly />
                    <input type="hidden" id="share_value" name="share_value" readOnly />

                    <div id="title" className="form-group">
                        Title:  
                        <input  className="form-control" type="text" name="idea_title" placeholder="Title your idea here."/>
                    </div>


                    <div id="content" className="form-group">
                        Explain your idea:    
                        <textarea rows="4" className="form-control" type="text" name="content" placeholder="My idea is/has..."></textarea>
                    </div>

                    Attachment:
                    <div className="custom-file">
                        <input id="customFile" className="custom-file-input" type="file" placeholder="Choose File"/>                        
                        <label id="customFileLabel" className="custom-file-label" htmlFor="customFile">Choose File, if needed</label>
                    </div>

                    <div className="form-group mt-3">
                        <button id="new_idea_submit" type="submit" className="btn btn-dark" onClick={(event) => this.newIdeaSubmit(event)}>OFFER IDEA</button>
                        <input type="button" id="new_idea_cancel" className="btn btn-light" value="CANCEL" onClick={this.newIdeaCancel}/>
                    </div>
                </form>
            </div>
        );
    }
}

class CSRFToken extends React.Component{

    getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    render() {
        var csrftoken = this.getCookie('csrftoken');

        return (
            <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
        );
    };
}


// PAYMENT INFO PAGE

class NewCardParent extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            loading: false,
            cards: [],
        };
        this.getCustomerCards = this.getCustomerCards.bind(this);
        this.detachCard = this.detachCard.bind(this);
    }

    getCustomerCards() {
        fetch("/stripe/list_cards")
        .then(response => {
            return response.json();
        })
        .then(data => {
            this.setState({cards: data});
        })
    }

    detachCard(card_id){

        const url = "/stripe/detach_card/"+card_id
        fetch(url)
        .then(response => {
            if (response.status == 200){
                alert("Card Detached")
                this.getCustomerCards();
            }
        });

    }

    componentDidMount() {
        document.getElementById("change_pay_btn").addEventListener("click", () => {
            document.getElementById("select_credit_card").hidden = false;
            document.getElementById("credit_cards_box").hidden = false;
        });
        this.getCustomerCards();
    }

    render() {
        const cards = this.state.cards;
        var list_cards = [];
        Object.values(cards).map( entry => {
            list_cards.push(Object.values(entry));
        })

        return(
            <div className="container" >
                <div className="row justify-content-center" id="credit_cards_box" hidden>
                    <div className="col-6 col-lg-4">
                        {list_cards.map( (card, index) => <Select_Credit_Card key={index} card_id={card[0]} brand={card[1]} last4={card[2]} detach={this.detachCard} getCards={this.getCustomerCards}/>)}
                    </div>
                    <div className="col-6 col-lg-5">
                        <New_Credit_Card getCards={this.getCustomerCards}/>
                    </div>
                </div>
            </div>
        );
    }
}

class New_Credit_Card extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: false,
        }
    }


    componentDidMount() {
        
        //Stripe variable for stripe
        var stripe = Stripe('pk_test_51I1kZwF2Gy9eFZtoKSGPFTaP5BqN2Kg6Lt0UhJfAsCxa3aW0uwWuKvQuzYdFAiNks7UyVgcDVgOt83uWZosCx95o00H2ohFmeq');

        //mount element
        var elements = stripe.elements();
        var style = {

            base: {
              color: "#6C757D",
              fontWeight: 500,
              fontFamily: "Inter UI, Open Sans, Segoe UI, sans-serif",
              fontSize: "16px",
              fontSmoothing: "antialiased",
      
              "::placeholder": {
                color: "#17A2B8"
              }
            },
            invalid: {
              color: "#E25950"
            }
          }
        
        var card = elements.create("card", {style: style });
        var card_element="#card_element"
        card.mount(card_element);
    
    
        card.on('change', function(event) {
            var displayError = document.getElementById("card_errors");
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
            });
        
        var form_id = "setup_form"
        var paymentForm = document.getElementById(form_id)
        paymentForm.addEventListener("submit", (event) => this.setupForm(event, card, stripe));

    }

    async setupForm(event, card, stripe) {

        event.preventDefault();
        var clientSecret = await this.createCard();
        // console.log(clientSecret);
        const card_creation = await this.confirmCard(clientSecret, card, stripe);

        if (card_creation) {
            alert("Card Saved Successfully.")
            this.props.getCards();
        };

    }
       
    async createCard() {

        var url = "/stripe_create_card/"
        
        const response = await fetch(url);
        const responsejson = await response.json();
        var client_secret = responsejson.client_secret
    
        return await client_secret;
    }

    async confirmCard(clientSecret, card, stripe) {

        var cardholderName = document.getElementById('cardholder-name');
    
        const confirmation = await stripe.confirmCardSetup(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: cardholderName.value,
                }
            }
        }).then(function(result) {
            if (result.error) {
            // Show error to your customer (e.g. invalid card)
                alert(result.error.message);
                console.log(result.error.message);
                return false;
            } else {
            // The card has been created!
                return true;
            }
        });
        return confirmation;
    }

    render() {
        if (this.state.err) {
        //render element for loading error
            return (
                <div className="container text-center">
                    <div className="row">
                        <div className="col">
                            {this.state.err}.
                        </div>
                    </div>
                </div>
            );
        } else if (this.state.is_loading) {
            return (
                <div className="container text-left my-3 request-element">
                    <div className="row my-3">
                        <div className="col">
                            <div className="loader"></div>
                        </div>
                    </div>
                </div>
                );   
        } else {
            return (
                <div>
                    <div className="col text-center">
                            <input hidden id="client_secret"></input>

                            <input className="form-control text-center" id="cardholder-name" type="text" placeholder="Cardholder Name"></input>
                            <form className="my-2" id="setup_form">
                                <div id="card_element"></div>
                                <div id="card_errors" role="alert"></div>
                                <button className="btn btn-info my-2"id="card_btn">Save Card</button>
                            </form>
                    </div>
                </div>
            );
        }
    }
}

class Select_Credit_Card extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            is_loading: false,
        }
    }

    render() {
        if (this.state.err) {
            //render element for loading error
                return (
                    <div className="container text-center">
                        <div className="row">
                            <div className="col">
                                {this.state.err}.
                            </div>
                        </div>
                    </div>
                );
            } else if (this.state.is_loading) {
                return (
                    <div className="container text-left my-3 request-element">
                        <div className="row my-3">
                            <div className="col">
                                <div className="loader"></div>
                            </div>
                        </div>
                    </div>
                    );   
            } else {
                return (
                    <div>
                        <div className="row justify-content-left mb-2">
                                <div className="card_number">**** **** **** {this.props.last4}</div>
                                <button className="btn btn-outline-danger py-0" onClick={() => this.props.detach(this.props.card_id)}>Delete</button>
                        </div>
                    </div>
                );
            }
    }
}


// PAGINATOR ELEMENT

class Paginator extends React.Component {

    constructor(props){
        super(props);

    }

    previous_url (has_previous, actual_page) {
        if (has_previous){
            document.getElementById("previous_btn").className = "page-item";
    
            var url = new URL(window.location.href);
            var search_params = url.searchParams;
    
            search_params.set('page', parseInt(actual_page)-1);
            url.search = search_params.toString();
            var new_url = url.toString();
            return new_url
        } else {
            return "#"
        }
    }

    next_url(has_next, actual_page) {
        if (has_next){
            document.getElementById("next_btn").className = "page-item";
    
            var url = new URL(window.location.href);
            var search_params = url.searchParams;
    
            search_params.set('page', parseInt(actual_page)+1);
            url.search = search_params.toString();
            var new_url = url.toString();
            return new_url
        } else {
            return "#"
        }
    }

    render() {
        return(
            <div>
                <nav aria-label="Paginator">
                    <ul className="pagination justify-content-end">
                        <li id="previous_btn" className="page-item disabled">
                            <a id="previous_anchor" className="page-link text" href={this.previous_url(this.props.has_previous, this.props.actual_page)}>Previous</a>
                        </li>
                        <li className="page-item"><span className="page-link" href="#">Page {this.props.actual_page} of {this.props.last_page}</span></li>
                        <li id="next_btn" className="page-item disabled">
                            <a id="next_anchor" className="page-link" href={this.next_url(this.props.has_next, this.props.actual_page)}>Next</a>
                        </li>
                    </ul>
                </nav>
            </div>
        );  
    }

}