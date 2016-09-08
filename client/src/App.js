import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import $ from 'jquery';
import { Router, Route, hashHistory } from 'react-router';
import {readCookie, getCSRF, isToday, getItemsCostSum} from './utils.js';

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
            items: [],
            sum: 0
        };
    },
    updateSum: function() {
        var sum = getItemsCostSum(this.state.items);
        this.setState({sum: sum});
    },
    handleLogin: function(e) {
        $.get(this.listLink, function (data) {
            this.setState({items: data, authorized: true, sum: getItemsCostSum(data)});
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
                this.updateSum();
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
                this.updateSum();
            }
        }
        if (!this.state.sending) {
            this.setState({sending: true});
            var csrfToken = readCookie('csrftoken');
            $.ajax({
                url: this.detailLink + id,
                type: 'PATCH',
                data: item,
                success: function(result) {
                    this.setState({sending: false});
                }.bind(this)
            });
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
                        sum={this.state.sum}
                        visible={this.state.authorized}/>
                </p>
            </div>
        );
    }
});

var List = React.createClass({
    getInitialState: function() {
        return {limit: 0, edit: false};
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
                <div className={this.props.sum > this.state.limit? 'limit_red': 'limit_green'}>
                    Day limit: <span>{this.state.limit}</span>
                    <input className={this.state.edit? '': 'hidden'} type="number" name="limit" onBlur={this.handleLimitChange}/>
                    <input type="button" name="edit" value="edit" onClick={()=> this.setState({edit: !this.state.edit})}/>
                </div>
                <p></p>
                Sum: {this.props.sum}
                <p></p>
                {listItems}
            </div>
        );
    }
});

var ListItem = React.createClass({
    getInitialState: function() {
        return {edit: false};
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
                <form>
                    <span>Date: {this.props.data.date}</span>
                    <input className={this.state.edit? '': 'hidden'} type="date" name="date" onBlur={this.handleUpdate}/>
                    <p></p>
                    <span>Time: {this.props.data.time}</span>
                    <input className={this.state.edit? '': 'hidden'} type="time" name="time" onBlur={this.handleUpdate}/>
                    <p></p>
                    <span>Text: {this.props.data.text}</span>
                    <input className={this.state.edit? '': 'hidden'} type="text" name="text" onBlur={this.handleUpdate}/>
                    <p></p>
                    <span>Cost: {this.props.data.cost}</span>
                    <input className={this.state.edit? '': 'hidden'} type="number" name="cost" onBlur={this.handleUpdate}/>
                    <p></p>
                    <input type="button" name="edit" value="edit" onClick={()=> this.setState({edit: !this.state.edit})}/>
                    <input type="button" name="delete" value="x" onClick={this.handleDelete}/>
                </form>
                </p>
                </li>
            </div>
        );
    }
});

export default App;
