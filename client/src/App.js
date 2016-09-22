import React from 'react';
import logo from './logo.svg';
import './App.css';
import $ from 'jquery';
import {readCookie, createCookie, isToday, getItemsCostSum} from './utils.js';

var App = React.createClass( {
    render: function() {
        return (
            <Expenses/>
        );
    }
})

var LoginView = React.createClass({
    getInitialState: function() {
        return {
            url: '/login/',
            authorized: false
        };
    },
    handleUpdate: function(e) {
        var targetState = {};
        targetState[e.target.name] = e.target.value;
        this.setState(targetState);
    },
    authorize: function(userId) {
        this.setState({authorized: true});
        this.props.handleLogin(userId);
    },
    componentDidMount: function() {
        $.ajax({
            url: '/login/',
            type: 'GET',
            success: function(result) {
                this.authorize(result.id);
            }.bind(this)
        });
    },
    handleSubmit: function() {
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
                this.authorize(result.id);
            }.bind(this),
        });
    },
    render: function() {
        return (
            <div className={this.state.authorized? 'hidden' : ''}>
                <form>
                <input type="text" name="username" value={this.state.username} onChange={this.handleUpdate}/>
                <input type="password" name="password" value={this.state.password} onChange={this.handleUpdate}/>
                <input type="button" name="loginButton" value="Login" onClick={this.handleSubmit}/>
                </form>
            </div>
        );
    }
});

var Expenses = React.createClass({
    resourceLink: '/expenses/',
    getInitialState: function() {
        return {
            authorized: false,
            items: [],
            sum: 0
        };
    },
    updateSum: function() {
        var sum = getItemsCostSum(this.state.items);
        this.setState({sum: sum});
    },
    handleLogin: function(userId) {
        $.get(this.resourceLink, function (data) {
            this.setState({items: data, authorized: true, sum: getItemsCostSum(data), userId: userId});
        }.bind(this));
    },
    filterItems: function(filterState) {
        $.get(this.resourceLink, filterState,
            function (data) {
                this.setState({items: data, sum: getItemsCostSum(data)});
            }.bind(this)
        );
    },
    addItem: function() {
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', readCookie('csrftoken'));
            }.bind(this),
            url: this.resourceLink,
            data: {user: this.state.userId},
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
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader('X-CSRFToken', readCookie('csrftoken'));
                    }.bind(this),
                    url: this.resourceLink + item.id + '/',
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
                $.ajax({
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader('X-CSRFToken', readCookie('csrftoken'));
                    }.bind(this),
                    url: this.resourceLink + id + '/',
                    type: 'PATCH',
                    data: item,
                    success: function(result) {
                        this.setState({items: items});
                        this.updateSum();
                    }.bind(this)
                });
            }
        }
    },
    render: function() {
        return (
            <div className="App">
                <LoginView ref="loginView" handleLogin={this.handleLogin}></LoginView>
                <List
                        className={this.state.authorized? '': 'hidden'}
                        removeItem={this.removeItem}
                        addItem={this.addItem}
                        updateItem={this.updateItem}
                        filterItems={this.filterItems}
                        items={this.state.items}
                        sum={this.state.sum}
                        visible={this.state.authorized}/>
            </div>
        );
    }
});

var List = React.createClass({
    getInitialState: function() {
        return {
            limit: 0, edit: false, filter: false,
            filter_args: {
                'date_from': null,
                'date_to': null,
                'time_from': null,
                'time_to': null
            }};
    },
    handleLimitChange: function(e) {
        this.setState({limit: e.target.value});
    },
    handleFilterChange: function(e) {
        var currentFilterState = this.state.filter_args;
        currentFilterState[e.target.name] = e.target.value;
        this.props.filterItems(currentFilterState);
    },
    render: function() {
        var listItems = this.props.items.map(function(listItem) {
            return (
                <ListItem key={listItem.id} data={listItem}
                    removeItem={this.props.removeItem} updateItem={this.props.updateItem}/>
            );
        }.bind(this));
        return (
            <div>

            <nav className="navbar navbar-inverse">
                <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                    <div class="container-fluid">
                          <a href="#" className="navbar-brand"
                            name="addItem" onClick={this.props.addItem}>Add</a>

                          <FilteringModal modalId="filterModal" handleFilterChange={this.handleFilterChange}></FilteringModal>
                          <a href="#" className="navbar-brand"
                            name="toggleFilter" data-toggle="modal" data-target="#filterModal">Filter</a>


                          <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                              <form className="navbar-form navbar-left" role="search">
                                <div className="form-group">
                                  <input type="number" name="limit" onBlur={this.handleLimitChange} className="form-control" placeholder="Limit"/>
                                </div>
                              </form>
                          </div>
                    </div>
                </div>
            </nav>
                <h2 className={this.props.sum > this.state.limit? 'limit_red': 'limit_green'}> Sum: {this.props.sum} </h2>
                <p></p>
                <div className="bs-component">
                    <table className="table table-striped table-hover">
                        <thead>
                            <tr>
                                <td>Date</td>
                                <td>Time</td>
                                <td>Text</td>
                                <td>Cost</td>
                            </tr>
                        </thead>
                        <tbody>{listItems}</tbody>
                    </table>
                </div>
            </div>
        );
    }
});

var ListItem = React.createClass({
    getInitialState: function() {
        return {edit: false};
    },
    handleDelete: function(e) {
        this.props.removeItem(this.props.data);
    },
    render: function() {
        return (
            <tr>
                <td>{this.props.data.date}</td>
                <td>{this.props.data.time}</td>
                <td>{this.props.data.text}</td>
                <td>{this.props.data.cost}</td>
                <td>
                    <a href="#" className="btn btn-lg btn-success"
                        name="edit" data-toggle="modal" data-target={'#basicModal' + this.props.data.id}>edit</a>
                    <ListItemEditingModal
                        data={this.props.data}
                        updateItem={this.props.updateItem}/>
                </td>
                <td>
                    <a href="#" name="delete" className="btn btn-danger" onClick={this.handleDelete}>x</a>
                </td>
            </tr>

        );
    }
});

var ListItemEditingModal = React.createClass({
    getInitialState: function() {
        return this.props.data;
    },
    handleUpdate: function(e) {
        this.props.updateItem(this.props.data.id, e.target.name, e.target.value);
    },
    handleChange: function(e) {
        var newState = {};
        newState[e.target.name] = e.target.value;
        this.setState(newState);
    },
    render: function() {
        return (
            <div className="modal" id={'basicModal' + this.props.data.id} tabIndex="-1" role="dialog" aria-labelledby="basicModal" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-body">
                            <form className="form-horizontal">
                                <fieldset>
                                    <div className="form-group">
                                      <label htmlFor="date" className="col-lg-2 control-label">Date</label>
                                      <div className="col-lg-4">
                                         <input
                                            type="date" className="form-control" id="date" name="date"
                                            value={this.state.date}
                                            onBlur={this.handleUpdate}
                                            onChange={this.handleChange}/>
                                      </div>
                                    </div>

                                    <div className="form-group">
                                      <label htmlFor="time" className="col-lg-2 control-label">Time</label>
                                      <div className="col-lg-4">
                                          <input
                                                type="time" className="form-control" id="time" name="time"
                                                value={this.state.time}
                                                onBlur={this.handleUpdate}
                                                onChange={this.handleChange}/>
                                      </div>
                                    </div>

                                    <div className="form-group">
                                      <label htmlFor="text" className="col-lg-2 control-label">Text</label>
                                      <div className="col-lg-5">
                                          <input
                                                type="text" className="form-control" id="text" name="text"
                                                value={this.state.text}
                                                onBlur={this.handleUpdate}
                                                onChange={this.handleChange}/>
                                      </div>
                                    </div>

                                    <div className="form-group">
                                      <label htmlFor="cost" className="col-lg-2 control-label">Cost</label>
                                      <div className="col-lg-2">
                                          <input
                                                type="number" className="form-control" id="cost" name="cost"
                                                value={this.state.cost}
                                                onBlur={this.handleUpdate}
                                                onChange={this.handleChange}/>
                                      </div>
                                    </div>
                                </fieldset>
                            </form>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-default" data-dismiss="modal">OK</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});

var FilteringModal = React.createClass({
    render: function() {
        return (
            <div className="modal" id={this.props.modalId} tabIndex="-1" role="dialog" aria-labelledby="basicModal" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-body">
                            <form className="form-horizontal">
                                <fieldset>
                                    <div className="form-group">
                                      <label htmlFor="date_from" className="col-lg-2 control-label">Start Date</label>
                                      <div className="col-lg-4">
                                         <input
                                            type="date" className="form-control" id="date_from" name="date_from"
                                            onChange={this.props.handleFilterChange}/>
                                      </div>
                                    </div>

                                    <div className="form-group">
                                      <label htmlFor="date_to" className="col-lg-2 control-label">End Date</label>
                                      <div className="col-lg-4">
                                         <input
                                            type="date" className="form-control" id="date_to" name="date_to"
                                            onChange={this.props.handleFilterChange}/>
                                      </div>
                                    </div>

                                    <div className="form-group">
                                      <label htmlFor="time_from" className="col-lg-2 control-label">Start Time</label>
                                      <div className="col-lg-4">
                                         <input
                                            type="time" className="form-control" id="time_from" name="time_from"
                                            onChange={this.props.handleFilterChange}/>
                                      </div>
                                    </div>

                                    <div className="form-group">
                                      <label htmlFor="time_to" className="col-lg-2 control-label">End Time</label>
                                      <div className="col-lg-4">
                                         <input
                                            type="time" className="form-control" id="time_to" name="time_to"
                                            onChange={this.props.handleFilterChange}/>
                                      </div>
                                    </div>
                                </fieldset>
                            </form>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-default" data-dismiss="modal">OK</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});

export default App;
