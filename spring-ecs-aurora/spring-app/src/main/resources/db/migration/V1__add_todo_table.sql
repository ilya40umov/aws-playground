create table todo
(
    id   bigserial unique primary key,
    text text not null
);

insert into todo (text)
VALUES ('do something'),
       ('do something else'),
       ('do yet another thing');