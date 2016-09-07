import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import $ from 'jquery';
import { Router, Route, hashHistory } from 'react-router';
import {readCookie, getCSRF, isToday} from './utils.js';


var MainContainer = React.createClass({
    getInitialState: function() {
        return {
            authorized: false,
        };
    },
    handleLogin: function(e) {
        this.props.authorized = true;
        this.setState({authorized: true});
        this.refs.listView.toggleAuthorization(true);
        $.get('/core/items/', function (data) {
            this.refs.listView.setState({items: data});
            this.setState({items: data});
            this.refs.listView.forceUpdate();
        }.bind(this));

    },
    render: function() {
        return (
            <div className="App">
                <div className="App-header">
                    <h2>Expenses</h2>
                </div>
                <LoginView ref="loginView" handleLogin={this.handleLogin}></LoginView>
                <p className="App-intro">
                    <List ref="listView" url='/core/items/' items={this.state.items} visible={this.state.authorized}/>
                </p>
            </div>
        );
    }
});

var App = React.createClass( {
    render: function() {
        return (
            <Router history={hashHistory}>
                <Route path="/" component={MainContainer}/>
            </Router>
        );
    }
})

var LoginView = React.createClass({
    getInitialState: function() {
        return {
            url: '/core/login/',
            authorized: false
        };
    },
    handleUpdate: function(e) {
        var targetState = {};
        targetState[e.target.name] = e.target.value;
        this.setState(targetState);
    },
    handleSubmit: function() {
        this.props.handleLogin();
        $.ajax({
            crossDomain: true,
            xhrFields: {
                withCredentials: true
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', readCookie('csrftoken'));
            }.bind(this),
            url: this.state.url,
            type: 'POST',
            data: this.state,
            success: function(result) {
                this.setState({authorized: true});
            }.bind(this)
        });
    },
    render: function() {
        return (
            <div className={this.state.authorized? 'hidden' : ''}>
                <input type="text" name="username" value={this.state.username} onChange={this.handleUpdate}/>
                <input type="password" name="password" value={this.state.password} onChange={this.handleUpdate}/>
                <input type="button" name="loginButton" value="Login" onClick={this.handleSubmit}/>
            </div>
        );
    }
});


var List = React.createClass({
    getInitialState: function() {
        return {
            items: [],
            visible: false
        };
    },
    componentDidMount: function() {
        $.get(this.props.url, function (data) {
            this.setState({items: data});
        }.bind(this));
    },
    updateSum: function() {
        var sum = 0;
        var currentDate = new Date();
        for (var i = 0; i < this.state.items.length; i++) {
            var date = new Date(this.state.items[i].date);
            if (isToday(date)) {
                sum += this.state.items[i].cost;
            }
        }
        this.setState({sum: sum});
    },
    toggleAuthorization: function(authorized) {
        this.setState({visible: authorized});
    },
    handleAddItem: function() {
        var csrfToken = readCookie('csrftoken');
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            }.bind(this),
            url: this.props.url,
            type: 'POST',
            success: function(result) {
                this.state.items.push(result);
                this.forceUpdate();
            }.bind(this)
        });
    },
    handleItemRemove: function(item) {
        for(var i = 0; i < this.state.items.length; i++) {
            if (item.id == this.state.items[i].id) {
                this.state.items.splice(i, 1);
                this.forceUpdate();
                return;
            }
        }
    },
    handleLimitChange: function(e) {
        this.setState({limit: e.target.value});
    },
    render: function() {
        var listItems = this.state.items.map(function(listItem) {
            return (
                <ListItem data={listItem} handleItemRemove={this.handleItemRemove}/>
            );
        }.bind(this));
        this.updateSum();
        return (
            <ul className={this.state.visible? '': 'hidden'}>
                <button onClick={this.handleAddItem}>Add Item</button>
                <p></p>
                <div className={this.state.sum > this.state.limit? 'limit_red': 'limit_green'}>
                    Day limit: <input type="text" name="limit" value={this.state.limit} onChange={this.handleLimitChange}/>
                </div>
                <p></p>
                Sum: {this.state.sum}
                <p></p>
                {listItems}
            </ul>
        );
    }
})

var ListItem = React.createClass({
    getInitialState: function() {
        var data = this.props.data;
        data.url = "/core/item/" + data.id;
        data.sending = false;
        return data;
    },
    handleUpdate: function(e) {
        var targetState = {};
        targetState[e.target.name] = e.target.value;
        this.setState(targetState);
        if (!this.state.sending) {
            this.setState({sending: true});
            setTimeout(function() {
                $.ajax({
                    url: this.state.url,
                    type: 'PUT',
                    data: this.state,
                    success: function(result) {
                        this.setState({sending: false});
                    }.bind(this)
                });
            }.bind(this), 2000);
        }
    },
    handleDelete: function(e) {
        this.props.handleItemRemove(this.state);
        $.ajax({
            url: this.state.url,
            type: 'DELETE'
        });
    },
    render: function() {
        return (
            <div>
                <li>
                <p>
                <form action={"/core/item/" + this.state.id} method="PUT">
                    <input type="date" name="date" value={this.state.date} onChange={this.handleUpdate}/>
                    <input type="time" name="time" value={this.state.time} onChange={this.handleUpdate}/>
                    <input type="text" name="text" value={this.state.text} onChange={this.handleUpdate}/>
                    <input type="number" name="cost" value={this.state.cost} onChange={this.handleUpdate}/>
                    <input type="button" name="delete" value="x" onClick={this.handleDelete}/>
                </form>
                </p>
                </li>
            </div>
        );
    }
});

export default App;
