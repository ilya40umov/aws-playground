package me.ilya40umov.springapp

import org.springframework.data.repository.CrudRepository

interface TodoRepository : CrudRepository<Todo, Long>