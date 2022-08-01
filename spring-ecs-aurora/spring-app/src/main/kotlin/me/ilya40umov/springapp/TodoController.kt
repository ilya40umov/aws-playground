package me.ilya40umov.springapp

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class TodoController(
    private val todoRepository: TodoRepository
) {
    @GetMapping("/todos")
    fun list(): Iterable<Todo> = todoRepository.findAll()
}