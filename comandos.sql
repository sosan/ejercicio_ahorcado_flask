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


alter table records_ahorcado add constraint fk_id_usuario foreign key (id_usuario) references usuarios_ahorcado(id);

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
	hueco1 varchar(50),
	hueco2 varchar(50),
	hueco3 varchar(50),
    email_hueco1 varchar(50),
    email_hueco2 varchar(50),
    email_hueco3 varchar(50)
);




insert into sala(hueco1, hueco2, hueco3, email_hueco1, email_hueco2, email_hueco3) values ('','','', '','','')
