drop table if exists client, mailing, message;
create table mailing(
    id_mailing serial primary key,
    start_datetime timestamptz not null,
    text text not null,
    filter varchar(128),
    end_datetime timestamptz not null
);
create table client(
    id_client serial primary key,
    phone varchar(128) not null,
    code_phone varchar(64) not null,
    tag varchar(64),
    time_zone varchar(64) not null
);
create table message(
    id_message serial primary key,
    send_datetime timestamptz default null,
    status varchar(64) not null default 'not_send',
    id_mailing int not null,
    id_client int not null,
    constraint fk_mailing
    foreign key(id_mailing)
    references mailing(id_mailing)
    on delete cascade,
    constraint fk_client
    foreign key(id_client)
    references client(id_client)
    on delete cascade
);

insert into client (phone, code_phone, tag, time_zone)
values ('+79611234567', '861', 'a', 'NY'),
       ('+76543223344', '811', 'a', 'NY'),
       ('+23423423433', '823', 'a', 'NY'),
       ('+35454645656', '811', 'a', 'NY'),
       ('+79325354535', '555', 'a', 'NY'),
       ('+73423234234', '864', 'a', 'NY'),
       ('+79323423424', '134', 'a', 'MSK'),
       ('+79234242363', '442', 'a', 'MSK'),
       ('+79234234233', '111', 'b', 'MSK'),
       ('+73242342343', '111', 'b', 'MSK'),
       ('+79464656565', '111', 'b', 'MSK'),
       ('+79323123344', '111', 'b', 'MSK'),
       ('+79312122344', '111', 'b', 'MSK'),
       ('+79321111344', '111', 'b', 'MSK'),
       ('+79325555344', '111', 'b', 'MSK');

