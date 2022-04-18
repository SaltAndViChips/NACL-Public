CREATE TABLE IF NOT EXISTS guilds (
        GuildID integer PRIMARY KEY,
        Prefix text DEFAULT ","

);
CREATE TABLE IF NOT EXISTS users (
    UserID integer PRIMARY KEY,
    IsBanned  DEFAULT 0,
    NumWarn integer NOT NULL,
    NumBan integer DEFAULT 0,
    NumKick integer DEFAULT 0,
    LastWarn text Default "None",
    LastKick text Default "None",
    LastBan text Default "None",
    FOREIGN KEY (NumWarn) REFERENCES Warns(NumWarn)
);

CREATE TABLE IF NOT EXISTS warns (
    UserID integer PRIMARY KEY,
    GuildID integer,
    NumWarn integer DEFAULT 0,
    WarnReason text,
    WarnTime text,
    StaffID text
);

CREATE TABLE IF NOT EXISTS snipes (
    ID integer PRIMARY KEY,
    GuildID integer,
    UserID integer,
    Message text Default "Nothing has been deleted by this user yet!"
);

CREATE TABLE IF NOT EXISTS misc (
    LastSnipe integer,
    GuildID integer PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS blacklist (
    GuildID integer PRIMARY KEY,
    UserID integer

);

CREATE TABLE IF NOT EXISTS moods (
    UserID integer PRIMARY KEY,
    FirstMood text,
    SecondMood text,
    FirstRole text,
    SecondRole text

)