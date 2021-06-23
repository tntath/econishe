import os
import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader

COLUMN_MAINS = 'grid'
COLUMN_DATE = 'localminute'


class PowerDataset(Dataset):
    """Power dataset."""

    def __init__(self, path, device, start_date="2018-01-01", end_date="2018-02-16", should_normalize=True):
        """
        Args:
            path (string): Path to the csv file.
            device(string): the desired device.
            start_date: the first date e.g. '2016-04-01'.
            end_date: the last date e.g. '2017-04-01'.
        """

        self.mmax = None
        self.path = path
        self.device = device
        self.start_date = start_date
        self.end_date = end_date

        cols = [COLUMN_DATE, COLUMN_MAINS, device]
        data = pd.read_csv(path, usecols=cols)

        if self.start_date and self.end_date:
            data = data[(data[COLUMN_DATE] >= self.start_date) & (data[COLUMN_DATE] <= self.end_date)]

        mainchunk = data[COLUMN_MAINS]
        meterchunk = data[self.device]

        if should_normalize:
            mainchunk, meterchunk = self._normalize(mainchunk, meterchunk)
        self._fill_gaps(mainchunk, meterchunk)
        mainchunk, meterchunk = self._align_data(mainchunk, meterchunk)

        mainchunk = np.reshape(mainchunk, (mainchunk.shape[0], 1, 1))
        self.mainchunk = mainchunk
        self.meterchunk = np.reshape(meterchunk, (len(meterchunk), -1))

    def _align_data(self, mainchunk, meterchunk):
        ix = mainchunk.index.intersection(meterchunk.index)
        mainchunk = np.array(mainchunk[ix])
        meterchunk = np.array(meterchunk[ix])
        return mainchunk, meterchunk

    def _fill_gaps(self, mainchunk, meterchunk):
        mainchunk.fillna(0, inplace=True)
        meterchunk.fillna(0, inplace=True)

    def _normalize(self, mainchunk, meterchunk):
        if self.mmax == None:
            self.mmax = mainchunk.max()
        mainchunk = mainchunk / self.mmax
        meterchunk = meterchunk / self.mmax
        return mainchunk, meterchunk

    def __len__(self):
        return len(self.mainchunk)

    def __getitem__(self, i):
        x = torch.from_numpy(self.mainchunk)
        y = torch.from_numpy(self.meterchunk)
        return x[i], y[i]

    def __mmax__(self):
        return self.mmax


# dataset = PowerDataset(path='../data/house_7901.csv', device='microwave1')
# train_loader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=8)
# for i, data in enumerate(train_loader):
#     return i, x, y

