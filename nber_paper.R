library(tidyverse)
library(xkcd)
options(repr.plot.width=25, repr.plot.height=10)

get_data <- function(file_name) {
    df <- read_delim(file = file_name, delim = "|")
    df <- df %>% drop_na(id)
    return(df)
}

count_by_year <- function(df) {
    df <- df %>% drop_na(citation_date)
    df <- df %>% select(id, citation_date)
    df$year <- substr(df$citation_date, 1, 4)
    df <- df %>% group_by(year) %>% count()
    df$year <- as.integer(df$year)
    return(df)
}

published_paper <- function(df) {
    xrange <- range(df$year)
    yrange <- range(df$n)
    plot <- ggplot(data=df, aes(x=year, y=n, group=1)) +
        geom_line(size=1.5) +
        theme_xkcd() +
        xkcdaxis(xrange, yrange) +
        ggtitle("Total published papers by year") +
        theme(
            axis.text.x = element_text(size=rel(2)),
            axis.text.y = element_text(size=rel(2)),
            axis.title.x = element_text(size=rel(2)),
            axis.title.y = element_text(size=rel(2)),
            plot.title = element_text(size=30, hjust = 0.5)
        ) +
        scale_x_continuous(breaks = seq(min(df$year), max(df$year), by = 5)) +
        scale_y_continuous(breaks = seq(0, max(df$n), by = 200)) +
        xlab("Year") +
        ylab("Count")
    return(plot)
}
