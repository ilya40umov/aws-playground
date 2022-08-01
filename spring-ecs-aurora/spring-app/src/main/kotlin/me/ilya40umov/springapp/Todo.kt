package me.ilya40umov.springapp

import javax.persistence.Entity
import javax.persistence.GeneratedValue
import javax.persistence.GenerationType
import javax.persistence.Id

@Entity
data class Todo(
    @Id @GeneratedValue(strategy = GenerationType.AUTO)
    val id: Long,
    val text: String
)