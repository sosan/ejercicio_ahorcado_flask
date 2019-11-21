create database ahorcado;
use ahorcado;

create table usuarios_ahorcado
(
    id integer unsigned not null primary key auto_increment,
    nombre varchar(50),
    email varchar(50),
    clave varchar(50),
    current_hueco integer unsigned not null default 0
    

);



create table tipo_dificultad
(
    dificultad integer unsigned not null primary key,
    descripcion_dificultad varchar(50)
)
;



create table records_ahorcado
(
    id integer unsigned not null primary key auto_increment,
    record_single integer unsigned not null default 0,
    puntuacion_single integer unsigned not null default 0,
    record_multi  integer unsigned not null default 0,
    puntuacion_multi integer unsigned not null default 0,
    id_usuario integer unsigned not null


);

create table historico_puntuacion
(
    id integer unsigned not null primary key auto_increment,
    record_single integer unsigned not null default 0,
    puntuacion_single integer unsigned not null default 0,
    record_multi integer unsigned not null default 0,
    puntuacion_multi integer unsigned not null default 0,
    fecha timestamp not null default current_timestamp(),
    id_usuario integer unsigned not null

);



create table palabras_ahorcado
(
    id integer unsigned not null primary key auto_increment,
    categoria varchar(50),
    palabra varchar(50)
    

);





INSERT INTO usuarios_ahorcado(nombre, email, clave)
VALUES
("jose", "h@h.com", "123")
;

INSERT INTO records_ahorcado(record_single, puntuacion_single, record_multi, puntuacion_multi, id_usuario)
VALUES
(1000, 100, 2000, 200, 1)
;

INSERT INTO historico_puntuacion(record_single, puntuacion_single, record_multi, puntuacion_multi, id_usuario)
VALUES
(1000, 100, 2000, 200, 1)
;

insert into tipo_dificultad(dificultad, descripcion_dificultad)
values
(0, "noelegido"),
(5, "esqueleto"),
(4, "pulpo"),
(4, "estrella"),
(3, "zombi")
;


INSERT INTO palabras_ahorcado(categoria, palabra)
VALUES
("CIUDADES", "MEXICO"),
("CIUDADES", "MADRID"),
("CIUDADES", "PALMA"),
("COCHES", "AUDI"),
("PROGRAMACION", "PYTHON")
;


create table sala
(
	id integer unsigned not null primary key auto_increment,
	apodo_hueco1 varchar(50),
	apodo_hueco2 varchar(50),
	apodo_hueco3 varchar(50),
    email_hueco1 varchar(50), -- id del usuario en el hueco1
    email_hueco2 varchar(50), -- id del usuario en el hueco2
    email_hueco3 varchar(50), -- id en el usuairo en el hueco3
    fase_hueco1 integer unsigned not null default 0,
    fase_hueco2 integer unsigned not null default 0,
    fase_hueco3 integer unsigned not null default 0
);

insert into sala(apodo_hueco1, apodo_hueco2, apodo_hueco3, email_hueco1, email_hueco2, email_hueco3) values
('','','', '','','')
;

create table puntuacion_caracteres
(
    id integer unsigned not null primary key auto_increment,
    palabra varchar(1) not null,
    puntuacion integer unsigned not null
);


insert into puntuacion_caracteres(palabra, puntuacion)
values
('q', 50),
('w', 50),
('e', 5),
('r', 10),
('t', 50),
('y', 50),
('u', 5),
('i', 5),
('o', 5),
('p', 10),

('a', 0),
('s', 20),
('d', 20),
('f', 20),
('g', 20),
('h', 50),
('j', 10),
('k', 50),
('l', 10),
('ñ', 50),
('ç', 50),

('z', 50),
('x', 50),
('c', 10),
('v', 10),
('b', 10),
('n', 10),
('m', 10)

;

alter table records_ahorcado add constraint fk_id_usuario foreign key (id_usuario) references usuarios_ahorcado(id);


