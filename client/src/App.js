import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import $ from 'jquery';
import { Router, Route, hashHistory } from 'react-router';
import {readCookie, getCSRF, isToday} from './utils.js';

var App = React.createClass( {
    render: function() {
        return (
            <Router history={hashHistory}>
                <Route path="/" component={Expenses}/>
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

var Expenses = React.createClass({
    listLink: '/core/items/',
    detailLink: '/core/item/',
    getInitialState: function() {
        return {
            authorized: false,
            sending: false,
            items: []
        };
    },
    handleLogin: function(e) {
        $.get(this.listLink, function (data) {
            this.setState({items: data, authorized: true});
        }.bind(this));
    },
    addItem: function() {
        var csrfToken = readCookie('csrftoken');
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            }.bind(this),
            url: this.listLink,
            type: 'POST',
            success: function(result) {
                var items = this.state.items;
                items.push(result);
                this.setState({items: items});
            }.bind(this)
        });
    },
    removeItem: function(item) {
        var items = this.state.items;
        for(var i = 0; i < items.length; i++) {
            if (item.id == items[i].id) {
                items.splice(i, 1);
                this.setState({items: items});
                $.ajax({
                    url: this.detailLink + item.id,
                    type: 'DELETE'
                });
            }
        }
    },
    updateItem: function(id, key, value) {
        var items = this.state.items;
        var item = null;
        for(var i = 0; i < items.length; i++) {
            if (id == items[i].id) {
                items[i][key] = value;
                item = items[i];
                this.setState({items: items});
            }
        }
        if (!this.state.sending) {
            this.setState({sending: true});
            var csrfToken = readCookie('csrftoken');
            setTimeout(function() {
                $.ajax({
                    url: this.detailLink + id,
                    type: 'PATCH',
                    data: item,
                    success: function(result) {
                        this.setState({sending: false});
                    }.bind(this)
                });
            }.bind(this), 2000);
        }
    },
    render: function() {
        return (
            <div className="App">
                <div className="App-header">
                    <h2>Expenses</h2>
                </div>
                <LoginView ref="loginView" handleLogin={this.handleLogin}></LoginView>
                <p className="App-intro">
                    <List
                        className={this.state.authorized? '': 'hidden'}
                        removeItem={this.removeItem.bind(this)}
                        addItem={this.addItem.bind(this)}
                        updateItem={this.updateItem.bind(this)}
                        items={this.state.items}
                        visible={this.state.authorized}/>
                </p>
            </div>
        );
    }
});

var List = React.createClass({
    getInitialState: function() {
        return {};
    },
    getSum: function() {
        var sum = 0;
        var currentDate = new Date();
        for (var i = 0; i < this.props.items.length; i++) {
            var date = new Date(this.props.items[i].date);
            if (isToday(date)) {
                sum += parseInt(this.props.items[i].cost);
            }
        }
        this.setState({sum: sum});
        return sum;
    },
    handleLimitChange: function(e) {
        this.setState({limit: e.target.value});
    },
    render: function() {
        var listItems = this.props.items.map(function(listItem) {
            return (
                <ListItem data={listItem} removeItem={this.props.removeItem} updateItem={this.props.updateItem}/>
            );
        }.bind(this));
        return (
            <div>
                <button onClick={this.props.addItem}>Add Item</button>
                <p></p>
                <div className={this.state.sum > this.state.limit? 'limit_red': 'limit_green'}>
                    Day limit: <input type="text" name="limit" value={this.state.limit} onChange={this.handleLimitChange}/>
                </div>
                <p></p>
                Sum: {this.getSum()}
                <p></p>
                {listItems}
            </div>
        );
    }
});

var ListItem = React.createClass({
    getInitialState: function() {
        var data = this.props.data;
        data.url = "/core/item/" + data.id;
        data.sending = false;
        return data;
    },
    handleUpdate: function(e) {
        this.props.updateItem(this.props.data.id, e.target.name, e.target.value);
    },
    handleDelete: function(e) {
        this.props.removeItem(this.props.data);
    },
    render: function() {
        return (
            <div>
                <li>
                <p>
                <form method="PUT">
                    <input type="date" name="date" value={this.props.data.date} onChange={this.handleUpdate}/>
                    <input type="time" name="time" value={this.props.data.time} onChange={this.handleUpdate}/>
                    <input type="text" name="text" value={this.props.data.text} onChange={this.handleUpdate}/>
                    <input type="number" name="cost" value={this.props.data.cost} onChange={this.handleUpdate}/>
                    <input type="button" name="delete" value="x" onClick={this.handleDelete}/>
                </form>
                </p>
                </li>
            </div>
        );
    }
});

export default App;
