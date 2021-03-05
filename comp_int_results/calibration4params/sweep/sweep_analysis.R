library(ggplot2)
library(plot3D)
library(sqldf)
library(pracma)
library(contoureR)
library(rgl)
library(caret)
library(dplyr)
setwd("/Users/xarakas/Documents/2021/Dhmokritos/INFORE/February-2021/COIN-paper-results/calibration4params/sweep/")


#miguel_res_sweep <- read.csv(file = './sweep_log.log_frommac11.log')
res_sweep <- read.csv(file = '../../drug_discovery/sweep_log_eucl_dtw_l1-NORMALIZED-4params.log')

avg<-sqldf("select id, avg(k1) `k1`, avg(k2) `k2`, avg(k3) `k3`,  avg(k4) `k4`,
      sum(Eucl) `Eucl`, sum(Eucl_alive) `Eucl_alive`,
      sum(Eucl_apoptotic) `Eucl_apoptotic`,
      sum(Eucl_necrotic) `Eucl_necrotic`,
      sum(DTW) `DTW`, sum(DTW_alive) `DTW_alive`, sum(DTW_apoptotic) `DTW_apoptotic`,
      sum(DTW_necrotic) `DTW_necrotic`,
      sum(l1) `l1`, sum(l1_alive) `l1_alive`, sum(l1_apoptotic) `l1_apoptotic`,
      sum(l1_necrotic) `l1_necrotic`
      from res_sweep group by id")
  





write.csv(avg,"../../drug_discovery/sweep_per_individual_results_3dist.csv", row.names = FALSE)
alive_eucl=avg$Eucl_alive
apop_eucl=avg$Eucl_apoptotic
necr_eucl=avg$Eucl_necrotic
eucl=avg$Eucl
alive_dtw=avg$DTW_alive
apop_dtw=avg$DTW_apoptotic
necr_dtw=avg$DTW_necrotic
dtw=avg$DTW
alive_l1=avg$l1_alive
apop_l1=avg$l1_apoptotic
necr_l1=avg$l1_necrotic
l1=avg$l1

df_alive_eucl=data.frame(cbind(as.double(avg$Eucl_alive),'Alive', 'Euclidean'))
df_alive_eucl$X1<- as.character(df_alive_eucl$X1)
df_alive_eucl$X1<- as.double(df_alive_eucl$X1)

df_apop_eucl=data.frame(cbind(as.double(avg$Eucl_apoptotic),'Apoptotic', 'Euclidean'))
df_apop_eucl$X1<- as.character(df_apop_eucl$X1)
df_apop_eucl$X1<- as.double(df_apop_eucl$X1)

df_necr_eucl=data.frame(cbind(as.double(avg$Eucl_necrotic),'Necrotic', 'Euclidean'))
df_necr_eucl$X1<- as.character(df_necr_eucl$X1)
df_necr_eucl$X1<- as.double(df_necr_eucl$X1)

df_eucl=data.frame(cbind(as.double(avg$Eucl),'Sum', 'Euclidean'))
df_eucl$X1<- as.character(df_eucl$X1)
df_eucl$X1<- as.double(df_eucl$X1)

df_alive_dtw=data.frame(cbind(as.double(avg$DTW_alive),'Alive', 'DTW'))
df_alive_dtw$X1<- as.character(df_alive_dtw$X1)
df_alive_dtw$X1<- as.double(df_alive_dtw$X1)

df_apop_dtw=data.frame(cbind(as.double(avg$DTW_apoptotic),'Apoptotic', 'DTW'))
df_apop_dtw$X1<- as.character(df_apop_dtw$X1)
df_apop_dtw$X1<- as.double(df_apop_dtw$X1)

df_necr_dtw=data.frame(cbind(as.double(avg$DTW_necrotic),'Necrotic', 'DTW'))
df_necr_dtw$X1<- as.character(df_necr_dtw$X1)
df_necr_dtw$X1<- as.double(df_necr_dtw$X1)

df_dtw=data.frame(cbind(as.double(avg$DTW),'Sum', 'DTW'))
df_dtw$X1<- as.character(df_dtw$X1)
df_dtw$X1<- as.double(df_dtw$X1)


###########
df_alive_l1=data.frame(cbind(as.double(avg$l1_alive),'Alive', 'L1'))
df_alive_l1$X1<- as.character(df_alive_l1$X1)
df_alive_l1$X1<- as.double(df_alive_l1$X1)

df_apop_l1=data.frame(cbind(as.double(avg$l1_apoptotic),'Apoptotic', 'L1'))
df_apop_l1$X1<- as.character(df_apop_l1$X1)
df_apop_l1$X1<- as.double(df_apop_l1$X1)

df_necr_l1=data.frame(cbind(as.double(avg$l1_necrotic),'Necrotic', 'L1'))
df_necr_l1$X1<- as.character(df_necr_l1$X1)
df_necr_l1$X1<- as.double(df_necr_l1$X1)

df_l1=data.frame(cbind(as.double(avg$l1),'Sum', 'L1'))
df_l1$X1<- as.character(df_l1$X1)
df_l1$X1<- as.double(df_l1$X1)
#
#
#
allsamples<-data.frame(rbind(df_dtw,df_necr_dtw,df_apop_dtw,df_alive_dtw,df_l1,df_necr_l1,df_apop_l1,df_alive_l1,df_eucl,df_necr_eucl,df_apop_eucl,df_alive_eucl))
allsamples$X2<-as.factor(allsamples$X2)
allsamples$X3<-as.factor(allsamples$X3)

# ########
# ######## Used in paper
# #p <- ggplot(sample_n(allsamples,1600),  aes(x=X2, y=X1, fill=X3)) + 
 p <- ggplot(allsamples,  aes(x=X2, y=X1, fill=X3)) + 
   #p <- ggplot(allsamples,  aes(x=X2, y=X1, fill=X3)) + 
   #geom_violin(trim=TRUE) +
   geom_boxplot(width=1,outlier.alpha = 0.01, coef = 8) +
  scale_y_log10(
    breaks = scales::trans_breaks("log10", function(x) 10^x),
    labels = scales::trans_format("log10", scales::math_format(10^.x))
  ) +
   labs(x="Cell Category", y='Distance', fill='Distance Type') +
   theme(plot.title = element_text(hjust = 0.5))
 p

